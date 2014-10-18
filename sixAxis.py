#!/usr/bin/env python

import pygame
import time
from common import *

class sixAxis:
	connected = False
	
	def __init__(self):
		errorStr = "no sixAxis controller initialized. Check to make sure it is connected and correctly paired."
		searchStr = "PLAYSTATION(R)3 Controller"
		
		# init pygame
		pygame.init()
		
		numJoysticks = pygame.joystick.get_count()
		for i in range(0, numJoysticks):
			name = pygame.joystick.Joystick(i).get_name()
			if (name.find(searchStr) != -1):
				pygame.joystick.Joystick(i).init()
				log(pygame.joystick.Joystick(i).get_name() + " initialized")
				self.connected = True
				return
		# no sixAxis controller can be found
		log(errorStr)
		pygame.joystick.quit()
	
	# button map
	buttons = {
		0: 'select',
		1: 'L3',
		2: 'r3',
		3: 'start',
		4: 'dpad_up',
		5: 'dpad_right',
		6: 'dpad_down',
		7: 'dpad_left',
		8: 'L2',
		9: 'r2',
		10: 'L1',
		11: 'r1',
		12: 'triangle',
		13: 'circle',
		14: 'x',
		15: 'square',
		16: 'ps'
	}

	# axis map
	# up and right are positive for analog sticks L3 and r3
	# tilting forward/right is positive
	# button axes are force sensors with values 0-1, 0 being when lightly pressed, 1 when pressed in fully
	# axis 7 seems unused...
	axes = {
		0: ['L3_horizontal', 1],
		1: ['L3_vertical', -1],
		2: ['r3_horizontal', 1],
		3: ['r3_vertical', -1],
		4: ['tilt_leftright', 1], # value 0 when controller is level. this is rotation along axis going through centre of controller front to back
		5: ['tilt_backfront', 1], # value 0 when controller is level. this is rotation along axis going through centre of controller left to right
		6: ['tilt_combined', -1], # value -1 when level, 1 when flipped. this just combines axes 4 and 5
		8: ['dpad_up', 1],
		9: ['dpad_right', 1],
		10: ['dpad_down', 1],
		11: ['dpad_left', 1],
		12: ['L2', 1],
		13: ['r2', 1],
		14: ['L1', 1],
		15: ['r1', 1],
		16: ['triangle', 1],
		17: ['circle', 1],
		18: ['x', 1],
		19: ['square', 1]
	}
	
	def getEvents(self):
		eventList = {}
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.JOYBUTTONDOWN:
				eventList[self.buttons[event.button]] = { 'axisValue': -1 }
			if event.type == pygame.JOYAXISMOTION:
				eventList[self.axes[event.axis][0]] = { 'axisValue': self.axes[event.axis][1] * event.value }
		return eventList
		

# example output
'''
while True:
	events = sixAxis.getEvents()
	if events != None:
		for buttonName in events:
			print "button: " + buttonName + " axisValue: " + str(events[buttonName]['axisValue'])
	time.sleep(0.1)
'''
