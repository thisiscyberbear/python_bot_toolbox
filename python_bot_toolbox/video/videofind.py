import cv2
import numpy as np
import pyautogui
from python_bot_toolbox.image import *

# Function to capture a video of the screen
# @monitor: Defines the monitor from which the video should be captured - Default=1
def recordScreen_func(xcrop = -1, ycrop = -1, monitor = 1):
	# Get screen size
	[screenWidth, screenHeight] = imagefind.getScreenSize()
	# Should the video be cropped
	if xcrop != -1 and xcrop != -1:
		screenWidth = 
		screenHeight = 
	
	height, width, channels = screen.shape
	crop_screen = screen[int((height/2)-200):int((height/2)+200), int((width/2)-200):int((width/2)+200)]
	# display screen resolution, get it from your OS settings
	
	SCREEN_SIZE = (1920, 1080)
	# define the codec
	fourcc = cv2.VideoWriter_fourcc(*"mp4v")
	# create the video write object
	out = cv2.VideoWriter("output.mp4", fourcc, 20.0, (SCREEN_SIZE))
	while True:
		# Make a screenshot
		img = imagefind.takeScreenshot_func(color=cv2.COLOR_RGBA2RGB, monitor = monitor)
		# Convert to numpy array
		frame = np.array(img)
		# Write frame to video writer
		out.write(frame)
		# if the user clicks c, it exits
		if cv2.waitKey(1) == ord("c"):
			break

	# make sure everything is closed when exited
	cv2.destroyAllWindows()
	out.release()