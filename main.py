import time
from hexapodMotion import hexapodMotion
from sixAxis import sixAxis
from hcsr04 import hcsr04
import os

# initialize classes
hexapod = hexapodMotion()
sixAxis = sixAxis()
hcsr04 = hcsr04(1, 4) # i2c bus #1 and i2c device address 0x04. this connects to the ATmega328P


# vars used in follow-mode
bFollowModeEnabled = False
minFollowDistance = 5 # values in cm. these are the values to maintain in 'follow-mode' between the hexapod and an object in front using the ultrasonic sensor
maxFollowDistance = 50
followDistance = maxFollowDistance / 2 # the follow-mode distance to maintain
followModeWalkSpeed = 0.3 # value between 0-1 to affect the speed, higher being faster


# tmp variable to move the ping servo
pingServoValue = 350


# supporting functions


# modify the follow-mode ping distance to maintain. this changes based on dpad presses
def calcfollowDistance(direction):
	global followDistance
	if direction == 1 and followDistance < maxFollowDistance: followDistance += 1
	elif direction == -1 and followDistance > minFollowDistance: followDistance -= 1


# stand up
hexapod.stand()
print "hexapod standing up"
time.sleep(1)


# begin pinging. interval is determined in sixAxis class. defaults to 200ms
hcsr04.beginIntervalPinging()
time.sleep(0.2)

# debugging
#hexapod.walkSpeed = 0.3
#hexapod.testMode = True

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
			pingServoValue += 5
			hexapod.pwmL.setPWM(1, 0, pingServoValue)
			print pingServoValue
		if buttonName == 'dpad_right':
			pingServoValue -= 5
			hexapod.pwmL.setPWM(1, 0, pingServoValue)
			print pingServoValue
		if buttonName == 'start':
			os.system('flite -voice kalit -t "i am ah robot"&')
		if buttonName == 'select':		
			bFollowModeEnabled = not bFollowModeEnabled
			# in follow mode, make it walk at a specific speed
			if bFollowModeEnabled:
				print "follow mode enabled"
				hexapod.walkSpeed = followModeWalkSpeed
			else:
				print "follow mode disabled"
				hexapod.walkSpeed = 0
			
		
		if buttonName == 'r3_vertical' and bFollowModeEnabled == False: hexapod.walkSpeed = events[buttonName]['axisValue']
		
		
	# check if follow-mode is enabled
	if bFollowModeEnabled == True:
		objectDistance = hcsr04.getPingDistance()
		print objectDistance
		if objectDistance - followDistance > 5:
			print "walking forward"
			hexapod.walkSpeed = followModeWalkSpeed 
			hexapod.walk()
		if objectDistance - followDistance < -5:
			print "walking backward"
			hexapod.walkSpeed = -followModeWalkSpeed 
			hexapod.walk()
	else:
			hexapod.walk()