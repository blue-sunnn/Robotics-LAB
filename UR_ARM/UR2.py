import socket, time

# Define the IP address of the Universal Robot controller
ip = '10.10.0.61'  # replace by the IP address of the UR robot
# Define the port for the Robotiq gripper
g_port = 63352  # PORT used by robotiq gripper
# Define the port for the real-time client interface
# Port 30003 is used for sending URScript commands to the e-Series controller
port_rtde = 30003 # PORT used by UR robot for RTDE communication

def main():
    # Create a TCP/IP socket for the robot
    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the robot controller on the RTDE port
    r.connect((ip, port_rtde))

    # Create a separate TCP/IP socket for the gripper
    g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the gripper's port
    g.connect((ip, g_port))
    # Send an initial 'GET ACT' command to check the gripper's activation status
    g.send(b'GET ACT\n') 

    # Send a 'movej' (joint move) command to the robot
    # 'd2r()': converts degrees to radians for the joint position

    # Move to initial position
    r.send(b'movej([d2r(-90), d2r(-90), d2r(-90), d2r(-90), d2r(90), d2r(0)], 1, 0.25, 0, 0)\n')
    time.sleep(1)

    # Activate the gripper
    # Receive the response from the 'GET ACT' command
    g_recv = str(g.recv(10), 'UTF-8')
    if '1' in g_recv: # Check if the response contains '1', which means it's already activated
        print('Gripper Activated')

    print('get ACT  == ' + g_recv)
    # Send a 'GET POS' command to read the gripper's current position
    g.send(b'GET POS\n')
    g_recv = str(g.recv(10), 'UTF-8') # Read the response

    if g_recv:
        # Send 'SET ACT 1' to activate the gripper
        g.send(b'SET ACT 1\n')
        g_recv = str(g.recv(255), 'UTF-8')
        print(g_recv)
        time.sleep(3)
        # Send 'SET GTO 1' to enable "Go To" mode, allowing it to move to position requests
        g.send(b'SET GTO 1\n')
        # Send 'SET SPE 255' to set the gripper speed to maximum (0-255)
        g.send(b'SET SPE 255\n')
        # Send 'SET FOR 127' to set the gripper force to half (0-255)
        g.send(b'SET FOR 127\n')

    # Go to the first position
    r.send(b'movel(p[-0.18721, -0.37783, 0.03977, 0.415, -3.114, 0], 1.2, 0.4, 0, 0)\n')
    time.sleep(2)
    # Move down Z-axis to reach the object
    r.send(b'movel(p[-0.18721, -0.37783, 0.00077, 0.415, -3.114, 0], 1.2, 0.4, 0, 0)\n')
    time.sleep(2)

    # Close the gripper
    # Send 'SET POS 150' to close the gripper to position 150 (0=Full Open, 255=Full Close)
    g.send(b'SET POS 150\n') 
    g_recv = str(g.recv(255), 'UTF-8')
    print(g_recv)
    time.sleep(2)

    # Move up Z-axis with the object
    r.send(b'movel(p[-0.18721, -0.37783, 0.14004, 0.415, -3.114, 0], 1.2, 0.4, 0, 0)\n')
    time.sleep(2)
    # Move to the second position
    r.send(b'movel(p[-0.01220, -0.26895, 0.14004, 0.415, -3.114, 0], 1.2, 0.4, 0, 0)\n')
    time.sleep(2)
    # Move down Z-axis with the object
    r.send(b'movel(p[-0.01220, -0.26895, 0.00077, 0.415, -3.114, 0], 1.2, 0.4, 0, 0)\n')
    time.sleep(2)

    # Open the gripper
    # Send 'SET POS 0' to fully open the gripper and release the object
    g.send(b'SET POS 0\n')
    g_recv = str(g.recv(255), 'UTF-8')
    print(g_recv)
    time.sleep(2)

    # Close the gripper
    g.send(b'SET POS 150\n')
    g_recv = str(g.recv(255), 'UTF-8')
    print(g_recv)
    time.sleep(2)

    # Move up Z-axis with the object
    r.send(b'movel(p[-0.01220, -0.26895, 0.14004, 0.415, -3.114, 0], 1.2, 0.4, 0, 0)\n')
    time.sleep(2)
    # Move back to the first position
    r.send(b'movel(p[-0.18721, -0.37783, 0.14004, 0.415, -3.114, 0], 1.2, 0.4, 0, 0)\n')
    time.sleep(2)
    # Move down Z-axis with the object
    r.send(b'movel(p[-0.18721, -0.37783, 0.00077, 0.415, -3.114, 0], 1.2, 0.4, 0, 0)\n')
    time.sleep(2)

    # Open the gripper
    g.send(b'SET POS 0\n')
    g_recv = str(g.recv(255), 'UTF-8')
    print(g_recv)
    time.sleep(2)


if __name__ == '__main__':
    import sys
    main()