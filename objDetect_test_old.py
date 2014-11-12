import time
import picamera
import numpy as np
import Image
import io
import copy


imageParams = {
	'width': 320,
	'height': 240,

	# the boundary points for the pixel analysis loop
	'col_max': 320,
	'row_max': 240,
	'startRow': 0,
	'startCol': 0,

	# the imageParams['stream'] object to capture to
	'stream': io.BytesIO()
}


def processImage(imageParams):


	# rewind the imageParams['stream'] for reading
	imageParams['stream'].seek(0)


	# load the data to a numpy array
	image = np.fromstring(imageParams['stream'].getvalue(), dtype=np.uint8).reshape((imageParams['height'], imageParams['width'], 3))
	image2 = copy.deepcopy(image)




	# pixel test parameters
	pixelTestParams = {
		0: { 'testVal': 120, 'dir': 1 }, # red pixel
		1: { 'testVal': 120, 'dir': 1 }, # green pixel
		2: { 'testVal': -60, 'dir': -1 } # blue pixel
	}
	numTests = len(pixelTestParams)

	# increment to the next test in the dict
	def nextTestNum(x):
		x += 1
		if x == numTests: return 0
		else: return x

		

	t = time.time()

	
	# scan the image
	minSquareSearchSize = 6 # square search block in pixels 
	numRowsScanned = 0 # this is so that we can start at an arbitrary row
	detectedPoints = [] # the set of detected points satisfying the pixel criteria pixelTestParams
	numPtsFound = 0 # number of detectedPoints
	testNum = 2 # keep track of which test failed. defaults to 2 (the requirement on the B pixel)


	numI = 0 # number of tests performed

	rowOfLastFound = imageParams['height'] + 2 # if a set of points were found set this to the row number. when no points are found for x rows the loop will end
	
	i = imageParams['startRow']  # start row. this is so in successive frames we can start at a predicted row to reduce computation
	while numRowsScanned < imageParams['row_max']:
		if i > imageParams['height']: i = 0 # wrap to the first row if the end was reached

		ptsFoundCurrentRow = []
		colOfLastFound = imageParams['width'] + 2
		j = imageParams['startCol']
		while j < imageParams['col_max']:
			# perform the pixel colour tests
			#numI += 1
			image2[i][j] = [255, 255, 255]
			if pixelTestParams[testNum]['dir'] * image[i][j][testNum] >= pixelTestParams[testNum]['testVal']: # test 1
				testNum = nextTestNum(testNum)
				if pixelTestParams[testNum]['dir'] * image[i][j][testNum] >= pixelTestParams[testNum]['testVal']: # test 2
					testNum = nextTestNum(testNum)
					if pixelTestParams[testNum]['dir'] * image[i][j][testNum] >= pixelTestParams[testNum]['testVal']: # test 3
						if int(image[i][j][0]) - int(image[i][j][2]) > 80 and int(image[i][j][1]) - int(image[i][j][2]) > 80 : # test if it is not a proper shade
							ptsFoundCurrentRow.append(j)
							if len(ptsFoundCurrentRow) == 3:
								tmp = ptsFoundCurrentRow[0] - minSquareSearchSize
								if tmp > 0: imageParams['startCol'] = tmp
								else: imageParams['startCol'] = ptsFoundCurrentRow[0]
							rowOfLastFound = i
							colOfLastFound = j
							#image[i][j] = [0, 0, 0]
							image2[i][j] = [0, 0, 0]
							detectedPoints.append([i, j])
							numPtsFound = len(detectedPoints)
						
			if numPtsFound != 0 and (j - colOfLastFound) > 2 * minSquareSearchSize : # no points for 2 consecutive search cols. only care to find one object at a time so break the loop
				tmp = j + minSquareSearchSize
				if tmp < imageParams['width']: imageParams['col_max'] = tmp
				else: imageParams['col_max'] = imageParams['width']
				break 			
			j += minSquareSearchSize
		if numPtsFound != 0 and (i - rowOfLastFound) > 2 * minSquareSearchSize : break # no points for 2 consecutive search rows. only care to find one object at a time so break the loop
		i += minSquareSearchSize
		numRowsScanned += minSquareSearchSize
		
	#print numI


	
	if numPtsFound != 0:
		# calculate approximate midpoint of balloon and the standard deviation
		mean = np.mean(detectedPoints, axis=0) # midpoint
		print mean
		std = np.std(detectedPoints, axis=0) # used to predict the start row/column for the next image

		imageParams['startRow'] = int(mean[0] - 3 * std[0])
		imageParams['startCol'] = int(mean[1] - 3 * std[1])
		#imageParams['startRow'] = 0
		#imageParams['startCol'] = 0
		imageParams['col_max'] = imageParams['width']
		imageParams['row_max'] = imageParams['height']
		if imageParams['startRow'] < 0: imageParams['startRow'] = 0
		if imageParams['startCol'] < 0: imageParams['startCol'] = 0


	print str(time.time()) + ": Current estimated framerate: " + str(1 / (time.time() - t))


	# dump to file
	Image.fromarray(image2, 'RGB').save(str(time.time()) + ".png")


# loop to keep taking pictures and analyzing them
with picamera.PiCamera() as camera:
	camera.resolution = (imageParams['width'], imageParams['height'])
	camera.vflip = True # vertical flip
	#time.sleep(2)
	#camera.capture_sequence(imageParams['stream']Gen(), 'rgb', use_video_port=True) # capture in rgb format
	for stream in camera.capture_continuous(imageParams['stream'], 'rgb', use_video_port=True):
		processImage(imageParams)
		#time.sleep(0.01)

