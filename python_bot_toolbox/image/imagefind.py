from python_imagesearch.imagesearch import *
import pyautogui
from mss import mss
import cv2
import numpy as np
from PIL import Image

# All the 6 methods for cv2.matchTemplate comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

# Returns alpha channel mask of an image			
def getMask_func(image):
	channels = cv2.split(image)
	# Extract transparency channel
	alpha_channel = np.array(channels[3]) 
	# Generate mask image
	mask = cv2.merge([alpha_channel,alpha_channel,alpha_channel])
	return mask

# Find the location of one image on the screen
# Allows images with transparency
def imagefind_func(image, alpha=False, method=cv2.TM_CCORR_NORMED, threshold = 0.9, monitor = 1):
	# Capture Screenshot
	with mss() as sct:
		screen = np.asarray(sct.grab(sct.monitors[monitor]))
	screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2RGB)
	
	# Save shape of template image for debug
	h, w = image.shape[:-1]
	
	# Extract alpha channel if transparency is used
	if alpha:
		mask = getMask_func(image)
		# Remove alpha channel from input image
		image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
		# Remove alpha channel from screenshot
		screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2RGB)
		# Convert to grey scale
		#mask = cv2.cvtColor(mask, cv2.COLOR_RGB2RGB)

		# DEBUG
		# screen_rgb = screen_rgb.astype(np.uint8)
		# image_rgb = image_rgb.astype(np.uint8)
		# mask = mask.astype(np.uint8)
		# cv2.imwrite('mask.png',mask)
		# cv2.imwrite('test1.png',screen)
		# cv2.imwrite('test2.png',image)		
		# print(screen.dtype)
		# print(image.dtype)
		# print(mask.dtype)
		result = cv2.matchTemplate(screen, image, method, None, mask)
	else:
		# Create an grey scale image
		screen_gray = cv2.cvtColor(screen, cv2.COLOR_RGBA2RGB)
		image_gray = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
		# Compare input image with screenshot
		result = cv2.matchTemplate(screen_gray, image_gray, method)

	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)	
	# DEBUG
	print(min_val)
	print(max_val)
	print(min_loc)
	print(max_loc)
	
	if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
		if min_val <= threshold:
			top_left = min_loc
			bottom_right = (top_left[0] + w, top_left[1] + h)
			cv2.rectangle(screen,top_left, bottom_right, 255, 2)
			cv2.imwrite('res.png',screen)
			return [min_val, max_val, min_loc, max_loc]
			
	else:
		if max_val >= threshold:
			top_left = max_loc
			bottom_right = (top_left[0] + w, top_left[1] + h)
			cv2.rectangle(screen,top_left, bottom_right, 255, 2)
			cv2.imwrite('res.png',screen)
			return [min_val, max_val, min_loc, max_loc]				
	return [-1,-1,-1,-1]


# Find the location of one image on the screen
# Does not allow images with transparency
def scaledImagefind_func(image, scalefactor=10, useEdgeDetection=False, grey=False, method=cv2.TM_CCORR_NORMED, threshold = 0.9, monitor = 1):	
	# Capture Screenshot
	with mss() as sct:
		screen = np.asarray(sct.grab(sct.monitors[monitor]))
	h, w = image.shape[:-1]
	# Convert to grey scale or rgb
	if grey:
		screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	else:
		screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2RGB)
		image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
	
	# Detect edges - Use for rigid and well defined template images
	if useEdgeDetection:
		image = cv2.Canny(image, 50, 200)
	
	# DEBUG
	cv2.imwrite('test1.png',screen)
	cv2.imwrite('test2.png',image)
	
	found = None	
	for scale in np.linspace(0.2, 1.0, scalefactor)[::-1]:
		print(scale)
		# resize the screenshot according to the scale, and keep track
		# of the ratio of the resizing
		resized = imutils.resize(screen, width = int(screen.shape[1] * scale))
		r = screen.shape[1] / float(resized.shape[1])
		# if the resized image is smaller than the template, then break
		# from the loop
		if resized.shape[0] < tH or resized.shape[1] < tW:
			break
		# detect edges in the resized, grayscale image and apply template
		# matching to find the template in the image
		# Detect edges - Use for rigid and well defined template images
		if useEdgeDetection:
			image = cv2.Canny(resized, 50, 200)
		result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
		(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
		# check to see if the iteration should be visualized
		if args.get("visualize", False):
			# draw a bounding box around the detected region
			clone = np.dstack([edged, edged, edged])
			cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
				(maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
			cv2.imshow("Visualize", clone)
			cv2.waitKey(0)
		# if we have found a new maximum correlation value, then update
		# the bookkeeping variable
		if found is None or maxVal > found[0]:
			found = (maxVal, maxLoc, r)
	# unpack the bookkeeping variable and compute the (x, y) coordinates
	# of the bounding box based on the resized ratio
	(_, maxLoc, r) = found
	(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
	(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
	# draw a bounding box around the detected result and display the image
	cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
	cv2.imshow("Image", image)
	cv2.waitKey(0)
		
	return [-1,-1,-1,-1]

# Find the multiple locations of an image on the screen
def imagesfind_func(image, method=cv2.TM_CCOEFF_NORMED, threshold = 0.9, monitor = 1):
	# Capture Screenshot
	with mss() as sct:
		screen = np.asarray(sct.grab(sct.monitors[monitor]))			
	# Create an grey scale image
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

def test():
	print("Test123")
	return