# TODO
#
# return to initial position after no movement instead of staying mid-way through motion
# on start of walking, make sure movements are smooth and feet aren't dragging on ground to go to initial offset positions
# change standing to be smooth and to use combo femur/tibia movement instead of just femur (extend servo life)

import time
from hexapodMotion import hexapodMotion

motion = hexapodMotion()

walkSpeed = 1



motion.testServoOffsets()



'''
# stand up and wait for input
time.sleep(3)
motion.stand()



for x in range(10000): # parameter loop
	motion.walk(x)
	time.sleep(0.01 * walkSpeed)
'''
