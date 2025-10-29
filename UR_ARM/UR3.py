import socket, time

vs_ip = '10.10.0.222'       # IP address for the vision system (camera)
ip = '10.10.0.61'           # IP address of the UR robot
g_port = 63352              # Port used by the Robotiq gripper
port_rtde = 30003           # Port for UR robot RTDE communication
cam_port = 2025             # Port for the vision system (camera)

# Receives data from the vision system socket (v)
def recv():
    v_data = ''
    # Loop until data is received.
    while not (v_data := v.recv(20)): # The walrus operator (:=) assigns v.recv() to v_data
        time.sleep(0.1)
    # Decode the received bytes to a UTF-8 string and remove whitespace
    decoded = v_data.decode('utf-8').strip()
    # "X,Y" is received, convert to [Y_float, X_float]
    v_coor = list(map(float, {decoded.split(',')[1],decoded.split(',')[0]}))

    print('recv = ', v_coor)
    return v_coor # Return the list of coordinates
    

# Sends a command string to the vision system socket (v)
def send(cmd):
    # Encode the string as bytes and add a newline character, then send
    v.send(str.encode(cmd+'\n'))
    time.sleep(0.1)

def main():
    # Create a TCP/IP socket for the robot
    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the robot on the RTDE port
    r.connect((ip, port_rtde))

    # Create a separate TCP/IP socket for the gripper
    g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the gripper's port
    g.connect((ip, g_port))
    # Send an initial 'GET ACT' command to check the gripper's activation status
    g.send(b'GET ACT\n')


    global v # Declare 'v' as global so helper functions can access it
    try:
        # Create the socket for the vision system
        v = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        v.settimeout(10) # Set a 10-second timeout for the connection attempt
        # Connect to the vision system
        v.connect((vs_ip, cam_port))
        print(" Connected to vision " + vs_ip)
    except socket.timeout:
        print(" Timeout connecting to vision " + vs_ip) # Handle connection timeout
        sys.exit(1) # Exit the script
    except socket.error as e:
        print(f" Socket error: {e}") # Handle other socket errors
        sys.exit(1) # Exit the script
    

    # Move to initial position
    r.send(b'movel(p[-0.12757, -0.17303, 0.40000, 0, 3.142, 0], 1.2, 0.4, 0, 0)\n')
    time.sleep(2)

    # Activate the gripper
    g_recv = str(g.recv(10), 'UTF-8')
    if '1' in g_recv:
        print('Gripper Activated')

    print('get ACT  == ' + g_recv)
    g.send(b'GET POS\n')
    g_recv = str(g.recv(10), 'UTF-8')

    if g_recv:
        g.send(b'SET ACT 1\n')
        g_recv = str(g.recv(255), 'UTF-8')
        print(g_recv)
        time.sleep(3)
        g.send(b'SET GTO 1\n')
        g.send(b'SET SPE 255\n')
        g.send(b'SET FOR 200\n')

    send('cap!') # Send the "capture" trigger command to the vision system
    print("sent 'cap!'")

    # Receive the [Y, X] coordinates from the vision system
    difY, difX  = recv()

    # Open the gripper
    g.send(b'SET POS 0\n')
    g_recv = str(g.recv(255), 'UTF-8')
    print(g_recv)
    time.sleep(2)

    # Move to the object's X/Y position
    r.send(f'movel((pose_add(get_actual_tcp_pose(), p[{difX/1000}, {difY/1000-0.135}, 0, 0, 0, 0])), 1.2, 0.4, 0, 0)\n'.encode('utf-8'))
    time.sleep(1)
    # Move down in the Z-axis to the picking position
    r.send(f'movel((pose_add(get_actual_tcp_pose(), p[0, 0, -0.210, 0, 0, 0])), 1.2, 0.4, 0, 0)\n'.encode('utf-8'))
    time.sleep(1)

    # Close the gripper
    g.send(b'SET POS 175\n')
    g_recv = str(g.recv(255), 'UTF-8')
    print(g_recv)
    time.sleep(2)

    # Move up in the Z-axis with the object
    r.send(f'movel((pose_add(get_actual_tcp_pose(), p[0, 0, 0.210, 0, 0, 0])), 1.2, 0.4, 0, 0)\n'.encode('utf-8'))
    time.sleep(1)
    # Move to the drop-off position above the bin
    r.send(f'movel((pose_add(get_actual_tcp_pose(), p[-0.050, -0.050, 0, 0, 0, 0])), 1.2, 0.4, 0, 0)\n'.encode('utf-8'))
    time.sleep(1)
    # Move down in the Z-axis to the drop-off position
    r.send(f'movel((pose_add(get_actual_tcp_pose(), p[0, 0, -0.210, 0, 0, 0])), 1.2, 0.4, 0, 0)\n'.encode('utf-8'))
    time.sleep(1)

    # Open the gripper
    g.send(b'SET POS 0\n')
    g_recv = str(g.recv(255), 'UTF-8')
    print(g_recv)
    time.sleep(2)


if __name__ == '__main__':
    import sys
    main()