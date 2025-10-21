import math
import time

dType.SetPTPJointParams(api,200,200,200,200,200,200,200,200,0)
dType.SetPTPCoordinateParams(api,200,200,200,200,0)
dType.SetPTPJumpParams(api, 10, 200,0)
dType.SetPTPCommonParams(api, 100, 100,0)
moveX=0;moveY=0;moveZ=10;moveFlag=-1
pos = dType.GetPose(api)
x = pos[0]
y = pos[1]
z = pos[2]
rHead = pos[3]

# COIN 1
dType.SetEndEffectorSuctionCup(api, 1, 0, 1) 
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 200.479, -87.7465, -13.4501, rHead, 1)
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 199.9219, -84.3294, -59.8115, rHead, 1)
time.sleep(1)
dType.SetEndEffectorSuctionCup(api, 1, 1, 1) #suck the coin
time.sleep(1)
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 199.1656, -83.7937, -27.7555, rHead, 1)
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 298.972, -83.8716, -33.9704, rHead, 1)
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 301.3278, -83.7821, -53.0062, rHead, 1)
time.sleep(1)
dType.SetEndEffectorSuctionCup(api, 1, 0, 1)
time.sleep(1)
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 286.1234, -87.7337, 47.7324, rHead, 1)

# COIN 2
dType.SetEndEffectorSuctionCup(api, 1, 0, 1) 
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 251, -82.8006, 47.7324, rHead, 1)
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 251, -82.8006, -59.8115, rHead, 1)
time.sleep(1)
dType.SetEndEffectorSuctionCup(api, 1, 1, 1) #suck the coin
time.sleep(1)
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 251, -82.8006, -46.1723, rHead, 1)
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 298.972, -83.8716, -33.9704, rHead, 1)
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 302.5, -83, -43, rHead, 1)
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 302.5, -83, -52, rHead, 1)
time.sleep(1)
dType.SetEndEffectorSuctionCup(api, 1, 0, 1)
time.sleep(1)
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 286.1234, -87.7337, 47.7324, rHead, 1)

# COIN 3
dType.SetEndEffectorSuctionCup(api, 1, 0, 1) 
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 243, -87.7337, 47.7324, rHead, 1)
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 251, -30, 30, rHead, 1)
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 251, -30, -58.8534, rHead, 1)
time.sleep(1)
dType.SetEndEffectorSuctionCup(api, 1, 1, 1) #suck the coin
time.sleep(1)
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 251, -30, -43, rHead, 1)
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 251, -83.8716, -43, rHead, 1)
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 302.5, -83, -43, rHead, 1)
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 302.5, -83, -52, rHead, 1)
time.sleep(1)
dType.SetEndEffectorSuctionCup(api, 1, 0, 1)
time.sleep(1)
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 302.5, -83, 35, rHead, 1)