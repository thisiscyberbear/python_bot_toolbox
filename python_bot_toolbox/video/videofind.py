import cv2
import numpy as np
import pyautogui
import time, keyboard
from python_bot_toolbox.image import *

# Function to capture a video of the screen
# @fps: Frames per second for recording
# @monitor: Defines the monitor from which the video should be captured - Default=1
def recordScreen_func(fps = 25.0, monitor = 1):
	# Get screen size
	[screenWidth, screenHeight] = imagefind.getScreenSize()
	SCREEN_SIZE = (screenWidth, screenHeight)
	# define the codec
	fourcc = cv2.VideoWriter_fourcc(*"mp4v")
	# create the video write object
	out = cv2.VideoWriter("output.mp4", fourcc, fps, (SCREEN_SIZE))
	print("Recording started: %s" % time.ctime())
	while True:
		# Make a screenshot
		img = imagefind.takeScreenshot_func(color=cv2.COLOR_RGBA2RGB, monitor = monitor)
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