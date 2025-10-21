import socket
import time

vs_ip = '10.10.0.222'
ip = '10.10.0.61'  # replace by the IP address of the UR robot
g_port = 63352  # PORT used by robotiq gripper
port_rtde = 30003 # PORT used by UR robot for RTDE communication
cam_port = 2025

def recv():
    v_data = ''
    while not (v_data := v.recv(20)):
        time.sleep(0.1)
    decoded = v_data.decode('utf-8').strip()
    v_coor = list(map(float, {decoded.split(',')[1],decoded.split(',')[0]}))

    print('recv = ', v_coor)
    return v_coor
    
def send(cmd):
    v.send(str.encode(cmd+'\n'))
    time.sleep(0.1)

def main():
    # Robot  socket communication
    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r.connect((ip, port_rtde))

    # Gripper socket communication
    g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    g.connect((ip, g_port))
    g.send(b'GET ACT\n')

    global v
    try:
        v = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        v.settimeout(10)
        v.connect((vs_ip, cam_port))
        print(" Connected to vision " + vs_ip)
    except socket.timeout:
        print(" Timeout connecting to vision " + vs_ip)
        sys.exit(1)
    except socket.error as e:
        print(f" Socket error: {e}")
        sys.exit(1)
    

    # Move to initial position
    r.send(
        b'movel(p[-0.12757, -0.17303, 0.40000, 0, 3.142, 0], 1.2, 0.4, 0, 0)\n')
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

    send('cap!')
    print("sent 'cap!'")

    difY, difX  = recv()

    # Open the gripper
    g.send(b'SET POS 0\n')
    g_recv = str(g.recv(255), 'UTF-8')
    print(g_recv)
    time.sleep(2)

    r.send(f'movel((pose_add(get_actual_tcp_pose(), p[{difX/1000}, {difY/1000-0.135}, 0, 0, 0, 0])), 1.2, 0.4, 0, 0)\n'.encode('utf-8'))
    time.sleep(1)

    r.send(f'movel((pose_add(get_actual_tcp_pose(), p[0, 0, -0.210, 0, 0, 0])), 1.2, 0.4, 0, 0)\n'.encode('utf-8'))
    time.sleep(1)

    # Close the gripper
    g.send(b'SET POS 175\n')
    g_recv = str(g.recv(255), 'UTF-8')
    print(g_recv)
    time.sleep(2)

    r.send(f'movel((pose_add(get_actual_tcp_pose(), p[0, 0, 0.210, 0, 0, 0])), 1.2, 0.4, 0, 0)\n'.encode('utf-8'))
    time.sleep(1)

    r.send(f'movel((pose_add(get_actual_tcp_pose(), p[-0.050, -0.050, 0, 0, 0, 0])), 1.2, 0.4, 0, 0)\n'.encode('utf-8'))
    time.sleep(1)

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
