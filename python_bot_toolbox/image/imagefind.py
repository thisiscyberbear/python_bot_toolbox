from python_imagesearch.imagesearch import *
import pyautogui
import time
import keyboard
from mss import mss
import cv2
import numpy as np
import d3dshot

# Reload Loop: If no bullet is found on the screen a right click will be performed
def imagefind_func(image, foo=cv2.TM_SQDIFF_NORMED, threshold = 0.9):
	# Capture Screenshot
	with mss() as sct:
		screenshoot = sct.shot()
	result = cv2.matchTemplate(image, screenshot, method)
	loc = np.where(result >= threshold)		
			
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
	print(loc)
	print(min_val)
	print(max_val)
	print(min_loc)
	print(max_loc)
	for pt in zip(*loc[::-1]):
		cv2.rectangle(large_image, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

		#cv2.imwrite('res.png',large_image)
		#if loc.size:
			#print("Picture found")
		#if pos1[0] == -1:
			#print("Reload! %s" % time.ctime())
			#pyautogui.rightClick()
