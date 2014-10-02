import pygame
import time
import sys


# key and axis map
button_select 		= 0
button_L3 			= 1
button_r3 			= 2
button_start 		= 3
button_dpad_up 		= 4
button_dpad_right 	= 5
button_dpad_down 	= 6
button_dpad_left 	= 7
button_L2 			= 8
button_r2			= 9
button_L1			= 10
button_r1			= 11
button_triangle		= 12
button_circle		= 13
button_x			= 14
button_square		= 15
button_ps			= 16

axis_l3_horizontal		= 0
axis_l3_vertical		= 1
axis_r3_horizontal		= 2
axis_r2_vertical		= 3 # invert this
axis_tilt_horizontal	= 4
axis_tilt_vertical		= 5 # invert this

# there are some others here, translational acceleration probably but not very reliable

axis_dpad_up		= 8
axis_dpad_right		= 9
axis_dpad_down		= 10
axis_dpad_left		= 11
axis_l2				= 12
axis_r2				= 13
axis_l1				= 14
axis_r1				= 15
axis_triangle		= 16
axis_circle			= 17
axis_x				= 18
axis_square			= 19

class ps3Controller:

	def __init__(self):
		pygame.init()

		if pygame.joystick.get_count() == 0:
			print "ps3 controller not initialized"
			pygame.joystick.quit()
			sys.exit()

		j = pygame.joystick.Joystick(0)
		j.init()

		print "ps3 controller initialized"


# poll for input. accelerometer axes ignored
while True:
	events = pygame.event.get()
	for index, event in enumerate(events):
		if event.type == pygame.JOYBUTTONDOWN:
				print "button: " + str(event.button)
		if event.type == pygame.JOYAXISMOTION and event.axis not in range(4,7): # ignore the accelerometer axes
			print "axis: " + str(event.axis) + " " + str(event.value)
	time.sleep(0.1)
