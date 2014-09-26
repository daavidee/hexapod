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
