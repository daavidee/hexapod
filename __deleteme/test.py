from __future__ import division
from scipy.optimize import fsolve
import time 
import sys
import math
from Adafruit_PWM_Servo_Driver import PWM 


# initialise the PWM devices
pwmL = PWM(0x41, debug=True) # left side (view from rear)
pwmL.setPWMFreq(60) # Set frequency to 60 Hz 
pwmR = PWM(0x40, debug=True) # right side 
pwmR.setPWMFreq(60) # Set frequency to 60 Hz

#math functions, angle converted to degrees
def sin(angle):
	return math.sin(math.radians(angle))

def asin(x):
	return math.degrees(math.asin(x))
	
def cos(angle):
	return math.cos(math.radians(angle))
	
def tan(angle):
	return math.tan(math.radians(angle))

# absolute limits for servo travel
minPulseLen = 170 # Min pulse length out of 4096 (time HIGH) 
maxPulseLen = 580 # Max pulse length out of 4096 (time HIGH) 
servoMaxAngle = 120 # degrees subtended from minPulseLen to maxPulseLen 
	
	
# servo pulse length offsets
servoOffsets = { 
	"coxa1": 0,
	"coxa2": 20,
	"coxa3": 10,
	"coxa4": -15,
	"coxa5": 30,
	"coxa6": -5,
	"femur1": -10,
	"femur2": -20,
	"femur3": 25,
	"femur4": -25,
	"femur5": -5,
	"femur6": -5,
	"tibia1": -30,
	"tibia2": 25,
	"tibia3": 20,
	"tibia4": 0,
	"tibia5": -25,
	"tibia6": 10,
}

# leg 1 is the rear right leg (view from rear). leg number increasing ccw
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

# coxa positive movement ccw from top view (0 point with leg perpendicular to body), femur positive movement ccw from rearview (0 point parallel to floor), tibia positive movement ccw from rearview (0 point when right angle to femur)
servoMultipliers = { 
	"coxa1": -1,
	"coxa2": -1,
	"coxa3": -1,
	"coxa4": 1,
	"coxa5": 1,
	"coxa6": 1,
	"femur1": 1,
	"femur2": 1,
	"femur3": -1,
	"femur4": 1,
	"femur5": -1,
	"femur6": -1,
	"tibia1": 1,
	"tibia2": -1,
	"tibia3": -1,
	"tibia4": 1,
	"tibia5": 1,
	"tibia6": -1,
}
	
# servo functions
def getPulseLenFromAngle(legSection, angle):
	zeroDegPt = (minPulseLen + maxPulseLen) / 2
	diff = maxPulseLen - zeroDegPt
	pulseLen = zeroDegPt + servoMultipliers[legSection] * (diff * angle / (servoMaxAngle / 2) + servoOffsets[legSection])
	return int(round(pulseLen, 0))	
	
		
	
def moveToAngle(legSection, angle):
	servoChan = servoChans[legSection]
	legNum = int(legSection[-1:])
	pulseLen = getPulseLenFromAngle(legSection, angle)
	if 1 <= legNum <= 3:
		pwm = pwmR
	else:
		pwm = pwmL
	if minPulseLen <= pulseLen <= maxPulseLen:
		pwm.setPWM(servoChan, 0, pulseLen)
	else:
		print "servo " + legSection + " told to go to an out of range pos: " + str(pulseLen)
		

for i in range(1, 7):
	moveToAngle("femur" + str(i), 45)
	moveToAngle("tibia" + str(i), 60)








