import socket, time

robot_ip = '10.10.0.61'
port_rtde = 30003

r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r.connect((robot_ip, port_rtde))

while True:
    # Move to the first position
    r.send(b'movel((pose_add(get_actual_tcp_pose(), p[-0.1, 0, 0, 0, 0, 0])), 1.2, 0.4, 0, 0)\n')
    time.sleep(1)

    # Move to the second corner
    r.send(b'movel((pose_add(get_actual_tcp_pose(), p[0, 0.1, 0, 0, 0, 0])), 1.2, 0.4, 0, 0)\n')
    time.sleep(1)

    # Move to the third corner
    r.send(b'movel((pose_add(get_actual_tcp_pose(), p[0.1, 0, 0, 0, 0, 0])), 1.2, 0.4, 0, 0)\n')
    time.sleep(1)

    # Move back to the initial position
    r.send(b'movel((pose_add(get_actual_tcp_pose(), p[0, -0.1, 0, 0, 0, 0])), 1.2, 0.4, 0, 0)\n')
    time.sleep(1)
