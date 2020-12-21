import cv2
import numpy as np
import pyautogui
import time, keyboard
from python_bot_toolbox.image import *

# Function to capture a video of the screen
# @xcrop: Coordinates of the upper left crop point
# @ycrop: Coordinates of the lower right crop point
# @monitor: Defines the monitor from which the video should be captured - Default=1
def recordScreen_func(xcrop = (-1, -1), ycrop = (-1, -1), monitor = 1):
	# Get screen size
	[screenWidth, screenHeight] = imagefind.getScreenSize()
	# Should the video be cropped
	cropped = False
	if xcrop != (-1, -1) and ycrop != (-1, -1):
		if ycrop[0] < xcrop[0] or ycrop[1] < xcrop[1]:
			print("The y-crop point needs to be lower and to the right of the x-crop point!!!")
			return
		screenWidth = ycrop[0] - xcrop[0]
		screenHeight = ycrop[1] - xcrop[1]
	
	SCREEN_SIZE = (screenWidth, screenHeight)
	# define the codec
	fourcc = cv2.VideoWriter_fourcc(*"mp4v")
	# create the video write object
	out = cv2.VideoWriter("output.mp4", fourcc, 20.0, (SCREEN_SIZE))
	print("Recording started: %s" % time.ctime())
	while True:
		# Make a screenshot
		img = imagefind.takeScreenshot_func(color=cv2.COLOR_RGBA2RGB, monitor = monitor)
		# Crop image if defined
		if cropped:
			img = img[xcrop[1]:ycrop[1], xcrop[0]:ycrop[0]]
		# Convert to numpy array
		frame = np.array(img)
		# Write frame to video writer
		out.write(frame)
		# Stop Record if 'c' key is pressed 
		if keyboard.is_pressed('c'):  
			print("Stopped by user")
			break
		
	# make sure everything is closed when exited
	cv2.destroyAllWindows()
	out.release()
	print("Recording stopped: %s" % time.ctime())