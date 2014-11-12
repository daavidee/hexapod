import time
import picamera
import numpy as np
import Image
import io
import copy
import sys

# set recursion depth higher than the default of 1000. will avoid with tweaking later
sys.setrecursionlimit(2000)


imageParams = {
	'width': 320,
	'height': 240,

	# the initial points for the pixel analysis loop
	'startRow': 0,
	'startCol': 0,
	
	'minSquareSearchSize': 6, # square search block in pixels 

	# the imageParams['stream'] object to capture to
	'stream': io.BytesIO()
}


# pixel test parameters
pixelTestParams = {
	0: { 'testVal': 85, 'dir': 1 }, # red pixel
	1: { 'testVal': 85, 'dir': 1 }, # green pixel
	2: { 'testVal': -60, 'dir': -1 } # blue pixel
}
numTests = len(pixelTestParams)
testNum = 2 # keep track of which test failed. defaults to 2 (the requirement on the B pixel)


# add all tested pixels to this array
testedPixels = []

# recursively test pixels until the wrong colour is found or end of image is reached
def rDetectPixels(im, i, j):
	if i >= imageParams['height']: return
	if j >= imageParams['width']: return
	if testPixel(im, i, j) == True:
		im[i][j] = [0, 0, 0]
		rDetectPixels(im, i, j - imageParams['minSquareSearchSize'] )
		rDetectPixels(im, i, j + imageParams['minSquareSearchSize'] )
		rDetectPixels(im, i - imageParams['minSquareSearchSize'], j)
		rDetectPixels(im, i + imageParams['minSquareSearchSize'], j)
	


# increment to the next test in the dict
def nextTestNum(x):
	x += 1
	if x == numTests: return 0
	else: return x

# test if pixel satisfies the pixelTestParams
def testPixel(im, i, j):
	'''
	global testNum
	if pixelTestParams[testNum]['dir'] * im[i][j][testNum] >= pixelTestParams[testNum]['testVal']: # test 1
		testNum = nextTestNum(testNum)
		if pixelTestParams[testNum]['dir'] * im[i][j][testNum] >= pixelTestParams[testNum]['testVal']: # test 2
			testNum = nextTestNum(testNum)
			if pixelTestParams[testNum]['dir'] * im[i][j][testNum] >= pixelTestParams[testNum]['testVal']: # test 3
	'''
	
	if int(im[i][j][0]) - int(im[i][j][2]) > 80 and int(im[i][j][1]) - int(im[i][j][2]) > 80 : # test if it is not a proper shade
		#im[i][j] = [0, 0, 0]
		return True
	#im[i][j] = [255, 255, 255]
	return False
		


def processImage(imageParams):
	
	# rewind the imageParams['stream'] for reading
	imageParams['stream'].seek(0)


	# load the data to a numpy array
	image = np.fromstring(imageParams['stream'].getvalue(), dtype=np.uint8).reshape((imageParams['height'], imageParams['width'], 3))
	image2 = copy.deepcopy(image)


	t = time.time()

	
	# scan the image
	numRowsScanned = 0 # this is so that we can start at an arbitrary row but still wrap around if necessary
	detectedPoints = [] # the set of detected points satisfying the pixel criteria pixelTestParams



	numI = 0 # number of tests performed


	
	# flag to break through all loops (will make into a function after)
	bBreakLoop = False
	
	# loop to crudely find the object. will recursively identify all points after the object is found
	i = imageParams['startRow']  # start row. this is so in successive frames we can start at a predicted row to reduce computation
	while i < imageParams['height'] -1:
		if i > imageParams['height']: i = 0 # wrap to the first row if the end was reached

		ptsFoundCurrentRow = []
		if i == imageParams['startRow']: j = imageParams['startCol']
		else: j = 0
		while j < imageParams['width']:
			# perform the pixel colour tests
			#numI += 1

			
			if testPixel(image2, i, j) == True:
				
				detectedPoints.append([i, j])
				ptsFoundCurrentRow.append(j)
				if len(ptsFoundCurrentRow) == 3: # 3 consecutive points found, assume object is found
					bBreakLoop = True
					break
				image2[i][j] = [0, 0, 0]

						
			j += imageParams['minSquareSearchSize']
			
		if bBreakLoop: break
		i += imageParams['minSquareSearchSize']
		numRowsScanned += imageParams['minSquareSearchSize']
		
		
	if len(detectedPoints) == 0: imageParams['startRow'] = 0
	else:
		
		rDetectPixels(image2, i, j)
		
		
		# calculate approximate midpoint of balloon and the standard deviation
		mean = np.mean(detectedPoints, axis=0) # midpoint
		print mean
		std = np.std(detectedPoints, axis=0) # used to predict the start row/column for the next image

		imageParams['startRow'] = int(mean[0])
		imageParams['startCol'] = int(mean[1])
		
		if imageParams['startRow'] < 0: imageParams['startRow'] = 0
		if imageParams['startCol'] < 0: imageParams['startCol'] = 0


	print str(time.time()) + ": Current estimated framerate: " + str(1 / (time.time() - t))


	# dump to file
	Image.fromarray(image2, 'RGB').save(str(time.time()) + ".png")


# loop to keep taking pictures and analyzing them
with picamera.PiCamera() as camera:
	camera.resolution = (imageParams['width'], imageParams['height'])
	camera.vflip = True # vertical flip
	camera.exposure_mode = 'night'
	#time.sleep(2)
	#camera.capture_sequence(imageParams['stream']Gen(), 'rgb', use_video_port=True) # capture in rgb format
	for stream in camera.capture_continuous(imageParams['stream'], 'rgb', use_video_port=True):
		processImage(imageParams)
		time.sleep(0.01)

