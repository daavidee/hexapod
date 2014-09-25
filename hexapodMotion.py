#!/usr/bin/python

from __future__ import division
from Adafruit_PWM_Servo_Driver import PWM 
from scipy.optimize import fsolve
import time 
import sys
import math

# math functions, angles in degrees
def sin(angle):
	return math.sin(math.radians(angle))

def asin(x):
	return math.degrees(math.asin(x))
	
def cos(angle):
	return math.cos(math.radians(angle))
	
def tan(angle):
	return math.tan(math.radians(angle))

	
# mechanical parameters in cm (between rotational points)
coxaFemurLen = 1.7
femurLen = 8.0
tibiaLen = 12.5

# global absolute limits for servo travel
minPulseLen = 170 # Min pulse length out of 4096 (time HIGH) 
maxPulseLen = 580 # Max pulse length out of 4096 (time HIGH) 

# coxa positive movement ccw from top view (0 point with leg perpendicular to body)
# femur positive movement ccw from rearview (0 point parallel to floor)
# tibia positive movement ccw from rearview (0 point when right angle to femur)
# leg 1 is the rear right leg (view from rear). leg number increasing ccw

# servo calibration values. order: minPulseLen, maxPulseLen, degrees at minPulseLen, degrees at maxPulseLen, degress offset
servoParameters = { 
	"coxa1": [376, 255, 0, 45, 0],
	"coxa2": [353, 255, 0, 40, 0],
	"coxa3": [365, 255, 0, 43, 0],
	"coxa4": [360, 455, 0, 29, 0],
	"coxa5": [401, 475, 0, 25, 0],
	"coxa6": [365, 475, 0, 35, 0],
	"femur1": [369, 575, 0, 75, 0],
	"femur2": [351, 568, 0, 77, 0],
	"femur3": [386, 192, 0, 73, 0],
	"femur4": [392, 580, 0, 67, 0],
	"femur5": [380, 180, 0, 75, 0],
	"femur6": [382, 170, 0, 69, 0],
	"tibia1": [340, 582, 0, 75, 0],
	"tibia2": [340, 180, 0, 75, 0],
	"tibia3": [359, 180, 0, 75, 0],
	"tibia4": [380, 582, 0, 75, 0],
	"tibia5": [347, 582, 0, 75, 0],
	"tibia6": [367, 180, 0, 75, 0]
}

# legs 1-3 on pwmR, 4-6 on pwmL
servoChans = {
	"coxa1": 0,
	"coxa2": 3,
	"coxa3": 11,
	"coxa4": 4,
	"coxa5": 12,
	"coxa6": 15,
	"femur1": 1,
	"femur2": 4,
	"femur3": 12,
	"femur4": 3,
	"femur5": 11,
	"femur6": 14,
	"tibia1": 2,
	"tibia2": 5,
	"tibia3": 13,
	"tibia4": 2,
	"tibia5": 10,
	"tibia6": 13,
}

# calculate servo pulse length for a desired angle. assume servo pulseLen is linear wrt angle
#calculate slope and y-intercept and do it that way. linear between the 2 points in servoParameters
def getPulseLenFromAngle(legSection, angle):
	totalSteps = servoParameters[legSection][1] - servoParameters[legSection][0]
	totalAngle = servoParameters[legSection][3] - servoParameters[legSection][2]
	slope = totalSteps / totalAngle
	intercept = servoParameters[legSection][0] - slope * servoParameters[legSection][2]
	pulseLen = slope * angle + intercept
	return int(round(pulseLen, 0))

class hexapodMotion:

	# initial parameters (i.e. while standing and default walking position)
	femurStandStartAngle = 30
	tibiaStandStartAngle = -20
	coxaStandStartAngle	= 0

	walkResolution = 60 # number of steps for one full walk cycle
	coxaWalkSweepAngle = 20 # half of the total sweep angle

	def __init__(self):
		# initialise the PWM devices
		self.pwmL = PWM(0x41, debug=True) # left side (view from rear)
		self.pwmL.setPWMFreq(60) # Set frequency to 60 Hz 
		self.pwmR = PWM(0x40, debug=True) # right side 
		self.pwmR.setPWMFreq(60) # Set frequency to 60 Hz
		
		# calculated initial robot parameters
		self.robotHeight = self.calcHeight(self.femurStandStartAngle, self.tibiaStandStartAngle)
		self.initialWidth = self.calcWidth(self.robotHeight, self.femurStandStartAngle, self.tibiaStandStartAngle)
		
	def moveServoToAngle(self, legSection, angle):
		servoChan = servoChans[legSection]
		legNum = int(legSection[-1:])
		pulseLen = getPulseLenFromAngle(legSection, angle)
		if 1 <= legNum <= 3:
			pwm = self.pwmR
		else:
			pwm = self.pwmL
		if minPulseLen <= pulseLen <= maxPulseLen:
			print "servo " + legSection + " told to go to pos: " + str(pulseLen)
			pwm.setPWM(servoChan, 0, pulseLen)
		else:
			print "servo " + legSection + " told to go to an out of range pos: " + str(pulseLen)
	
	# mainly for debugging	
	def moveServoToPos(self, legSection, pulseLen):
		servoChan = servoChans[legSection]
		legNum = int(legSection[-1:])
		if 1 <= legNum <= 3:
			pwm = self.pwmR
		else:
			pwm = self.pwmL
		if minPulseLen <= pulseLen <= maxPulseLen:
			pwm.setPWM(servoChan, 0, pulseLen)
	

	# walk supporting functions

	# vertical distance of tibia tip to femur/coxa pivot point (robot height)
	def calcHeight(self, femurAngle, tibiaAngle):
		return tibiaLen * cos(femurAngle + tibiaAngle) - femurLen * sin(femurAngle)

	# horizontal distance from tibia point on floor to femur pivot point. height is the vertical distance of tibia tip to femur/coxa pivot point
	def calcWidth(self, height, femurAngle, tibiaAngle):
		return femurLen * cos(tibiaAngle) / cos(femurAngle + tibiaAngle) + height * tan(femurAngle + tibiaAngle)

	# when coxa angle changes during walking, these are the femur and tibia angles to maintain robot height and position of tibia tip on floor without slipping
	def tibiaFemurWalkAngles(self, coxaAngle):
		d = self.initialWidth / cos(coxaAngle)
		def f(x):
			eqns = [tibiaLen*cos(x[0]+x[1]) - femurLen*sin(x[0]) - self.robotHeight]
			eqns.append(-d + femurLen*cos(x[1])/cos(x[0]+x[1]) + self.robotHeight*tan(x[0]+x[1]))
			return eqns
			
		f_roots = fsolve(f, [self.femurStandStartAngle, self.tibiaStandStartAngle], xtol = 0.5) # initial guesses are just the initial values
		return f_roots

	# degrees offset in the parameter loop for fluid leg movement while walking
	def coxaWalkLegOffset(self, leg):
		if leg == 1:   return -240
		elif leg == 2: return -120
		elif leg == 3: return 0
		elif leg == 4: return -300
		elif leg == 5: return -60
		elif leg == 6: return -180

		
	# angle of coxa during walking
	def walkServoAngles(self, leg, x):
		angles = {}
		interval = 360/walkResolution
		coxaServoAngle = coxaWalkSweepAngle * sin(x * interval + coxaWalkLegOffset(leg))
		walkAngle = x * interval + coxaWalkLegOffset(leg)
		if 90 < walkAngle % 360 < 270: 		# tibia in contact with ground
			angles["coxa"] = coxaWalkSweepAngle * sin(walkAngle)
			FTAngles = self.tibiaFemurWalkAngles(coxaAngle)
			angles["femur"] = FTAngles[0]
			angles["tibia"] = FTAngles[1]
			
		else:								# tibia not in contact with ground
			angles["coxa"] = coxaWalkSweepAngle * sin(180 + walkAngle)
			angles["femur"] = self.femurStandStartAngle + 20
		
		return angles

		
	# stand function
	def stand(self):
		for i in range(1, 7):
			self.moveServoToAngle("coxa" + str(i), self.coxaStandStartAngle)
			self.moveServoToAngle("femur" + str(i), self.femurStandStartAngle + 20)
		 
		time.sleep(1)
		for i in range(1, 7):
			self.moveServoToAngle("tibia" + str(i), self.tibiaStandStartAngle)
		
		time.sleep(1) 
		for i in range(1, 7):
			self.moveServoToAngle("femur" + str(i), self.femurStandStartAngle)
		time.sleep(1)

		
	# walk function
	def walk(self, x):
		t1 = time.time()
		for i in range(1, 7): # leg loop
			leg = str(i)
			
			# get the angles
			angles = self.walkServoAngles(leg, x, direction)
			
			# move the servos
			self.moveServoToAngle("coxa" + leg, angles["coxa"])
			self.moveServoToAngle("femur" + leg, angles["femur"])
			self.moveServoToAngle("tibia" + leg, angles["tibia"])
		print time.time() - t1
		
	def testServoOffsets(self):
		self.moveServoToPos("tibia6", 367)
		#self.pwmR.setPWM(12, 0, 580)
		#self.pwmL.setPWM(3, 0, 170)
		
		for i in range(1, 7):
			self.moveServoToAngle("coxa" + str(i), 0)
			self.moveServoToAngle("femur" + str(i), 50)
			#self.moveServoToAngle("tibia" + str(i), 45)
		