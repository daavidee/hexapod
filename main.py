import time
import math
from hexapodMotion import hexapodMotion
from sixAxis import sixAxis

# initialize classes
#motion = hexapodMotion()
sixAxis = sixAxis() 

# initial variables
currWalkValue = 0 # the r3_vertical value

# some supporting functions
def calcWalkSpeed():
	minWalkScale = 5
	maxWalkScale = 100
	tmp = int(math.fabs(currWalkValue * maxWalkScale))
	if tmp > maxWalkScale: tmp == maxWalkScale
	if tmp == 0: tmp = minWalkScale
	return (maxWalkScale - tmp)
	


# stand up and wait for input
time.sleep(3)
#motion.stand()
print "hexapod standing up"

# main parameter loop
x = 1 # parameter variable
while True:
	events = sixAxis.getEvents()
	for buttonName in events:
		if buttonName == 'r3_vertical': currWalkValue = events[buttonName]['axisValue']
	if currWalkValue > 0:
		print "walking forward"
		print x
		x += 1
	elif currWalkValue < 0:
		print "walking backward"
		print x
		x -= 1
		
	# motion.walk(x)
	time.sleep(0.001 * calcWalkSpeed())
	

#motion.testServoOffsets()