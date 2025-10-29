import socket, time

# Define the IP address of the Universal Robot controller
robot_ip = '10.10.0.61'
# Define the port for the real-time client interface
# Port 30003 is used for sending URScript commands to the e-Series controller
port_rtde = 30003

# Create a standard TCP/IP socket
r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the robot controller's server socket
r.connect((robot_ip, port_rtde))

while True:

    # 'movel' command: Moves the robot linearly to a target pose.
    # 'get_actual_tcp_pose()': Gets the robot's current TCP position and orientation.
    # 'pose_add(p1, p2)': Adds two poses together.
    # 'p[0, 0, 0, 0, 0, 0]': [x, y, z, Rx, Ry, Rz]
    # movel( pose, a, v, t, r ): a = tool acceleration(m/s^2), 
    #                            v = tool speed(m/s), 
    #                            t = time(s), 
    #                            r = blend radius(m)

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