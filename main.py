# TODO
# put parameter loop in hexapodMotion class instead 

import time
import math
import copy
from hexapodMotion import hexapodMotion
from sixAxis import sixAxis
from hcsr04 import hcsr04

# initialize classes
#motion = hexapodMotion()
sixAxis = sixAxis()
hcsr04 = hcsr04(1, 0x04) # i2c bus #1 and i2c device address 0x04. this connects to the ATmega328P

# initial variables
minWalkScale = 5 # this scales the r3_vertical value to affect the walk speed
maxWalkScale = 100
curWalkValue = 0 # the r3_vertical value

# vars used in follow-mode
followModeEnable = False
minFollowDistance = 5 # values in cm. these are the values to maintain in 'follow-mode' between the hexapod and an object in front using the ultrasonic sensor
maxFollowDistance = 50
followDistance = maxFollowDistance / 2 # the follow-mode distance to maintain
followModeWalkValue = 0.5 # value between 0-1 to affect the speed, higher being faster


# supporting functions

# modify the walking speed based on input from the right (r3) analog stick
def calcWalkSpeed():
	tmp = int(math.fabs(curWalkValue * maxWalkScale))
	if tmp > maxWalkScale: tmp == maxWalkScale
	if tmp == 0: tmp = minWalkScale
	return (maxWalkScale - tmp)

# modify the follow-mode ping distance to maintain. this changes based on dpad presses
def calcfollowDistance(direction):
	global followDistance
	if direction == 1 and followDistance < maxFollowDistance: followDistance += 1
	elif direction == -1 and followDistance > minFollowDistance: followDistance -= 1


# stand up
#time.sleep(3)
#motion.stand()
print "hexapod standing up"


# main parameter loop

x = 0 # parameter variable
hcsr04.beginIntervalPinging() # begin pinging. interval is determined in sixAxis class. defaults to 200ms
while True:
	# monitor for buttonpresses on sixaxis
	events = sixAxis.getEvents()
	for buttonName in events:
		if buttonName == 'dpad_up': 
			calcfollowDistance(1)
			print followDistance
		if buttonName == 'dpad_down': 
			calcfollowDistance(-1)
			print followDistance
		if buttonName == 'select':
			followModeEnable = not followModeEnable
			# in follow mode, make it walk faster
			if followModeEnable: curWalkValue = followModeWalkValue
			else: curWalkValue = 0
				
		if buttonName == 'r3_vertical': curWalkValue = events[buttonName]['axisValue']
		
		
	# check if follow-mode is enabled
	if followModeEnable == True:
		objectDistance = hcsr04.getPingDistance()
		print objectDistance
		if objectDistance == -1: print objectDistance
		if objectDistance - followDistance > 3:
			print "walking forward"
			x += 1
		if objectDistance - followDistance < -3:
			print "walking backward"
			x -= 1
	else:
		if curWalkValue > 0:
			print "walking forward"
			print x
			x += 1
		elif curWalkValue < 0:
			print "walking backward"
			print x
			x -= 1
		
	#print x
	#motion.walk(x)
	time.sleep(0.001 * calcWalkSpeed())
	

#motion.testServoOffsets()