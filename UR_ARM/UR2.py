import socket
import time
import binascii

ip = '10.10.0.61'  # replace by the IP address of the UR robot
g_port = 63352  # PORT used by robotiq gripper
port_rtde = 30003 # PORT used by UR robot for RTDE communication


def main():
    # Robot  socket communication
    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r.connect((ip, port_rtde))

    # Gripper socket communication
    g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    g.connect((ip, g_port))
    g.send(b'GET ACT\n')

    # Move to initial position
    r.send(
        b'movej([d2r(-90), d2r(-90), d2r(-90), d2r(-90), d2r(90), d2r(0)], 1, 0.25, 0, 0)\n')
    time.sleep(1)

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
        g.send(b'SET FOR 127\n')

    # Go to the first position to pick the object
    r.send(
        b'movel(p[-0.18721, -0.37783, 0.03977, 0.415, -3.114, 0], 1.2, 0.4, 0, 0)\n')
    time.sleep(2)

    # Close the gripper
    g.send(b'SET POS 150\n')
    g_recv = str(g.recv(255), 'UTF-8')
    print(g_recv)
    time.sleep(2)

    # Move up Z-axis with the object
    r.send(
        b'movel(p[-0.18721, -0.37783, 0.14004, 0.415, -3.114, 0], 1.2, 0.4, 0, 0)\n')
    time.sleep(2)

    # Move to the second position
    r.send(
        b'movel(p[-0.01220, -0.26895, 0.14004, 0.415, -3.114, 0], 1.2, 0.4, 0, 0)\n')
    time.sleep(2)

    # Move down Z-axis with the object
    r.send(
        b'movel(p[-0.01220, -0.26895, 0.04004, 0.415, -3.114, 0], 1.2, 0.4, 0, 0)\n')
    time.sleep(2)

    # Open the gripper
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
    r.send(
        b'movel(p[-0.01220, -0.26895, 0.14004, 0.415, -3.114, 0], 1.2, 0.4, 0, 0)\n')
    time.sleep(2)

    # Move back to the first position
    r.send(
        b'movel(p[-0.18721, -0.37783, 0.14004, 0.415, -3.114, 0], 1.2, 0.4, 0, 0)\n')
    time.sleep(2)

    # Move down Z-axis with the object
    r.send(
        b'movel(p[-0.18721, -0.37783, 0.03977, 0.415, -3.114, 0], 1.2, 0.4, 0, 0)\n')
    time.sleep(2)

    # Open the gripper
    g.send(b'SET POS 0\n')
    g_recv = str(g.recv(255), 'UTF-8')
    print(g_recv)
    time.sleep(2)


if __name__ == '__main__':
    import sys
    main()
