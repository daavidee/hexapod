import math

coxaFemurLen = 1.7
femurLen = 8.0
tibiaLen = 12.5

# math functions, angles in degrees
def sin(angle):
	return math.sin(math.radians(angle))

def asin(x):
	return math.degrees(math.asin(x))
	
def cos(angle):
	return math.cos(math.radians(angle))
	
def tan(angle):
	return math.tan(math.radians(angle))

class test:
	g = 5
	def __init__(self):
		self.robotHeight = self.calcHeight(self.femurStandStartAngle, self.tibiaStandStartAngle)
	def t1(self, x):
		return x*y
	def t2(self, x):
		return self.g * x
	def calcHeight(self, femurAngle, tibiaAngle):
		return tibiaLen * cos(femurAngle + tibiaAngle) - femurLen * sin(femurAngle)
	femurStandStartAngle = 20
	tibiaStandStartAngle = -20
	
		
servoParameters = { 
	"coxa1": [60, 2],
}
print abs(-108)
		
		
