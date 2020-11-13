import pyautogui
from mss import mss
import cv2
import imutils
import numpy as np
from PIL import Image

# All the 6 methods for cv2.matchTemplate comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
			
# Displays the Screen Size of the primary monitor and returns it 	
def getScreenSize():
	screenWidth, screenHeight = pyautogui.size()
	print("Width: " + str(screenWidth) + " Height: " + str(screenHeight))
	return [screenWidth, screenHeight]

# Displays the current mouse position and returns it 
def getCurrentMousePos():
	currentMouseX, currentMouseY = pyautogui.position()
	print("X-Pos: " + str(currentMouseX) + " Y-Pos: " + str(currentMouseY))
	return [currentMouseX, currentMouseY]

# Displays the current mouse position each second for a defined duration
# @seconds: Duration of the function in seconds
# @timeSleep: Duration of pause between two requests 
def getCoordinatesLoop(seconds, timeSleep=1):
	for x in range(seconds):
		getCurrentMousePos()
		time.sleep(timeSleep)
		
# Returns alpha channel mask of an image	
# @image: Input image which has an alpha channel		
def getMask_func(image):
	channels = cv2.split(image)
	# Extract transparency channel
	alpha_channel = np.array(channels[3]) 
	# Generate mask image
	mask = cv2.merge([alpha_channel,alpha_channel,alpha_channel])
	return mask

# Returns an image of the current screen		
# @color: Define color scheme of the screenshot
# @monitor: Define monitor from which the screenshot should be taken
def takeScreenshot_func(color=cv2.COLOR_RGBA2RGB, monitor = 1):
	# Capture Screenshot
	with mss() as sct:
		screen = np.asarray(sct.grab(sct.monitors[monitor]))
	# Remove alpha channel if set
	if color==cv2.COLOR_RGBA2RGB:
		screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2RGB)
	return screen
	

# Find the location of one image on the screen
# Allows images with transparency
# @image: Input image which will be searched
# @screen: Input image of the screen
# @alpha: Does the input image contains an alpha channel (transparency) - Default=False
# @useEdgeDetection: Should edge detection be used for the search - Default=False
# @gray: Should an gray scaled image be used for the search - Default=False
# @method: Detection method for the search - Default=cv2.TM_CCORR_NORMED
# @threshold: Threshold for detecting an image - Default=0.9
# @debug: Debug mode with more output - Default=False
def imagefind_func(image, screen, alpha=False, useEdgeDetection=False, gray=False, method=cv2.TM_CCORR_NORMED, threshold = 0.9, debug=False):
	# Save shape of template image for debug
	h, w = image.shape[:-1]
	
	# Extract alpha channel if transparency is used
	if alpha:
		mask = getMask_func(image)
		# Detect edges - Use for rigid and well defined template images
		if useEdgeDetection:
			image = cv2.Canny(image, 50, 200)
			screen = cv2.Canny(screen, 50, 200)
		if gray:
			# Remove alpha channel from input image and convert to gray scale
			image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			# Remove alpha channel from screenshot and convert to gray scale
			screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
			# Remove alpha channel from mask and convert to gray scale
			mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
		else:
			# Remove alpha channel from input image
			image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
			# Remove alpha channel from screenshot
			screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2RGB)

		# DEBUG
		if debug:
			cv2.imwrite('mask.png',mask)
			cv2.imwrite('test1.png',screen)
			cv2.imwrite('test2.png',image)		
			print(screen.dtype)
			print(image.dtype)
			print(mask.dtype)
		result = cv2.matchTemplate(screen, image, method, None, mask)
	else:
		# Detect edges - Use for rigid and well defined template images
		if useEdgeDetection:
			image = cv2.Canny(image, 50, 200)
			screen = cv2.Canny(screen, 50, 200)
		# Create an gray scale image
		if gray:
			# Remove alpha channel from input image
			image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			# Remove alpha channel from screenshot
			screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
		else:
			# Remove alpha channel from input image
			image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
			# Remove alpha channel from screenshot
			screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2RGB)
		# Compare input image with screenshot
		result = cv2.matchTemplate(screen, image, method)

	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)	
	# DEBUG
	if debug:
		print(min_val)
		print(max_val)
		print(min_loc)
		print(max_loc)
		
	
	if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
		if min_val <= threshold:
			if debug:
				top_left = min_loc
				bottom_right = (top_left[0] + w, top_left[1] + h)
				cv2.rectangle(screen,top_left, bottom_right, 255, 2)
				cv2.imwrite('res.png',screen)
			return [min_val, max_val, min_loc, max_loc, result]
			
	else:
		if max_val >= threshold:
			if debug:
				top_left = max_loc
				bottom_right = (top_left[0] + w, top_left[1] + h)
				cv2.rectangle(screen,top_left, bottom_right, 255, 2)
				cv2.imwrite('res.png',screen)
			return [min_val, max_val, min_loc, max_loc, result]				
	return [-1,-1,-1,-1,-1]


# Find the location of one image on the screen
# @image: Input image which will be searched
# @screen: Input image of the screen
# @scalefactor: Number of scales which will be performed - Default=10
# @alpha: Does the input image contains an alpha channel (transparency) - Default=False
# @useEdgeDetection: Should edge detection be used for the search - Default=False
# @gray: Should an gray scaled image be used for the search - Default=False
# @method: Detection method for the search - Default=cv2.TM_CCORR_NORMED
# @threshold: Threshold for detecting an image - Default=0.9
# @debug: Debug mode with more output - Default=False
def scaledImagefind_func(image, screen, scalefactor=10, alpha=False, useEdgeDetection=False, gray=False, method=cv2.TM_CCORR_NORMED, threshold = 0.9, debug=False):	
	# Save size of template image
	h, w = image.shape[:-1]
	
	# DEBUG
	if debug:
		cv2.imwrite('test1.png',screen)
		cv2.imwrite('test2.png',image)
	
	found = None	
	for scale in np.linspace(0.2, 1.0, scalefactor)[::-1]:
		# Calculate the round
		round = int(np.round((1.0-scale)/(0.8/(scalefactor-1))))
		# Resize screenshot according to  scale
		resized = imutils.resize(screen, width = int(screen.shape[1] * scale))
		r = screen.shape[1] / float(resized.shape[1])
		# Stop if resized image is smaller than the template
		if resized.shape[0] < h or resized.shape[1] < w:
			break
			
		min_val, max_val, min_loc, max_loc, result = imagefind_func(image, resized, alpha=alpha, useEdgeDetection=useEdgeDetection, gray=gray, method=method, threshold = threshold, debug=False)
		# Save if a new min/max was found
		if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
			if found is None or (min_val < found[0] and min_val is not -1):
				found = (min_val, min_loc, r, result, round)
		else:
			if found is None or max_val > found[0]:
				found = (max_val, max_loc, r, result, round)
	
	# Calculate the original (x, y) coordinates
	if found is not None and found[0] is not -1:
		(value, location, r, result, round) = found
		(startX, startY) = (int(location[0] * r), int(location[1] * r))
		(endX, endY) = (int((location[0] + w) * r), int((location[1] + h) * r))
		# DEBUG
		if debug:
			print(value)
			print(location)
			print(r)
			print((startX, startY))
		if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
			if value <= threshold:
				if debug:
					top_left = (startX, startY)
					bottom_right = (top_left[0] + w, top_left[1] + h)
					cv2.rectangle(screen,top_left, bottom_right, 255, 2)
					cv2.imwrite('res.png',screen)
				return [value, -1, (startX, startY), -1, result, round]
				
		else:
			if value >= threshold:
				if debug:
					top_left = (startX, startY)
					bottom_right = (top_left[0] + w, top_left[1] + h)
					cv2.rectangle(screen,top_left, bottom_right, 255, 2)
					cv2.imwrite('res.png',screen)
				return [-1, value, -1, (startX, startY), result, round]	
			
	return [-1,-1,-1,-1,-1,-1]

# Find the multiple locations of an image on the screen
# @image: Input image which will be searched
# @method: Detection method for the search - Default=cv2.TM_CCORR_NORMED
# @threshold: Threshold for detecting an image - Default=0.9
# @monitor: Defines the input monitor - Default=1
def imagesfind_func(image, method=cv2.TM_CCOEFF_NORMED, threshold = 0.9, monitor = 1):
	# Capture Screenshot
	with mss() as sct:
		screen = np.asarray(sct.grab(sct.monitors[monitor]))			
	# Create an gray scale image
	screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
	# Compare input image with screenshot
	result = cv2.matchTemplate(screen_gray, image, method)
	loc = np.where(result >= threshold)	
	# DEBUG
	# print(loc)
	w, h = image.shape[::-1]
	for pt in zip(*loc[::-1]):
		cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
	cv2.imwrite('res.png',screen)
	return loc	
