import cv2
import numpy as np
import pyautogui


def recordScree_func():
	while True:
		# make a screenshot
		img = pyautogui.screenshot()
		# convert these pixels to a proper numpy array to work with OpenCV
		frame = np.array(img)
		# convert colors from BGR to RGB
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		# write the frame
		out.write(frame)
		# show the frame
		cv2.imshow("screenshot", frame)
		# if the user clicks q, it exits
		if cv2.waitKey(1) == ord("q"):
			break

	# make sure everything is closed when exited
	cv2.destroyAllWindows()
	out.release()