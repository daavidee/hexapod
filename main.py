#!/usr/bin/env python

from common import *
log("Starting imports")

import time
from hexapodMotion import hexapodMotion
from sixAxis import sixAxis
from hcsr04 import hcsr04

log("Initializing classes...")

hexapod = hexapodMotion()
sixAxis = sixAxis()
hcsr04 = hcsr04(0x01, 0x04) # i2c bus #1 and i2c device address 0x04. this will communicate to the ATmega328P


# vars used in follow-mode
bFollowModeEnabled = False
minFollowDistance = 5 # values in cm. these are the values to maintain in 'follow-mode' between the hexapod and an object in front using the ultrasonic sensor
maxFollowDistance = 50
followDistance = maxFollowDistance / 2 # the follow-mode distance to maintain
followModeWalkSpeed = 0.3 # value between 0-1 to affect the speed, higher being faster


# tmp variable holding the pulseLen for the servo mounted to the ultrasonic sensor
pingServoPulseLen = 350


# supporting functions

# modify the follow-mode ping distance to maintain. this changes based on dpad up/down presses
def calcfollowDistance(direction):
	global followDistance
	if direction == 1 and followDistance < maxFollowDistance: followDistance += 1
	elif direction == -1 and followDistance > minFollowDistance: followDistance -= 1


# debugging
#hexapod.walkSpeed = 0.3
hexapod.testMode = True	
	

# stand up
log("Hexapod standing up")
hexapod.stand()


log("Beginning interval pinging")
# begin pinging. interval is determined in sixAxis class. defaults to 200ms
hcsr04.beginIntervalPinging()
time.sleep(0.2)


log("Ready for input")
# main loop
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
		if buttonName == 'dpad_left':
			pingServoPulseLen += 5
			hexapod.pwmL.setPWM(1, 0, pingServoPulseLen)
			print pingServoPulseLen
		if buttonName == 'dpad_right':
			pingServoPulseLen -= 5
			hexapod.pwmL.setPWM(1, 0, pingServoPulseLen)
			print pingServoPulseLen
		if buttonName == 'start':
			say("i am ah robot")
		if buttonName == 'select':		
			bFollowModeEnabled = not bFollowModeEnabled
			# in follow mode, make it walk at a specific speed
			if bFollowModeEnabled:
				print "follow mode enabled"
				hexapod.walkSpeed = followModeWalkSpeed
			else:
				print "follow mode disabled"
				hexapod.walkSpeed = 0
		if buttonName == 'r3_vertical' and bFollowModeEnabled == False: 
			hexapod.walkSpeed = events[buttonName]['axisValue']
		
	
	# check if follow-mode is enabled
	if bFollowModeEnabled == True:
		objectDistance = hcsr04.getPingDistance()
		print objectDistance
		if objectDistance - followDistance > 3:
			hexapod.walkSpeed = followModeWalkSpeed 
		elif objectDistance - followDistance < -3:
			hexapod.walkSpeed = -followModeWalkSpeed
		else:
			hexapod.walkSpeed = 0
			
	# walk. currently the sleep timer to throttle execution is located in the walk function itself
	hexapod.walk()