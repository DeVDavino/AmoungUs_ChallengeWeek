import cv2
import numpy as np
cap = cv2.VideoCapture(1)

pts = []
while (1):

    # Take each frame
    ret, frame = cap.read()
    #change the color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Lower boundary values for HSV
    #Upper boundary values for HSV
    lower_red = np.array([0, 0, 255])
    upper_red = np.array([255, 255, 255])
    #create a mask using the selected color range
    mask = cv2.inRange(hsv, lower_red, upper_red)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)
    
    #create a circle around the mask within the frame
    cv2.circle(frame, maxLoc, 20, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow('Track Laser', frame)
    #maxLoc is the x,y values of the drawn circle around the laser
    print(maxLoc)

    #condition to terminate the code from running (q)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        Break

cap.release()