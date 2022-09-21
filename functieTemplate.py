import cv2
import numpy as np

#------------------------ Template Matching ----------------------------
def templateMatching(frame):
  # Load template image
  template = cv2.imread('data/red2.png',0)
  assert not isinstance(template,type(None)), 'image not found'
  w, h = template.shape[::-1]

  # Template matching method
  method = eval('cv2.TM_CCOEFF_NORMED')

  # Template matching
  templateFrame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
  templateFrame = cv2.resize(templateFrame, (768, 512))
  res = cv2.matchTemplate(templateFrame,template,method)
  
  data = [(0,0)]
  
  maxv = np.max(res)
  if maxv>0.80:
    # Coordinates
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    
    # Drawing bounding box and text
    cv2.rectangle(templateFrame,top_left, bottom_right, 255, 2)
    cv2.putText(templateFrame, 'Sus detected', (top_left[0],top_left[1]-10), 
              cv2.FONT_HERSHEY_PLAIN, 1.0, (255,255,255))

    # Getting centre of Among us
    rectx, recty = ((top_left[0]+bottom_right[0])/2, (top_left[1]+bottom_right[1])/2)
    rectcenter = int(rectx),int(recty)
    data[0] = rectcenter
    # Show centre in frame
    cv2.circle(templateFrame, rectcenter, 20, (255,255,255), 3)

    template = templateFrame[top_left[1]:top_left[1]+h,top_left[0]:top_left[0]+w]
    data.append(templateFrame)
  return templateFrame, data

#------------------------ Laser ----------------------------
def laserDetection(frame):
  #change the color space
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  laserFrame = frame.copy()

  #Lower boundary values for HSV
  #Upper boundary values for HSV
  lower_red = np.array([0, 0, 255])
  upper_red = np.array([255, 255, 255])
  #create a mask using the selected color range
  mask = cv2.inRange(hsv, lower_red, upper_red)
  (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)
  
  #create a circle around the mask within the frame
  cv2.circle(laserFrame, maxLoc, 20, (255, 255, 255), 2, cv2.LINE_AA)
  #maxLoc is the x,y values of the drawn circle around the laser

  return laserFrame, maxLoc

#------------------------ Main ----------------------------
# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")

# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  
  if ret == True:
    # Funcion calls here
    templateFrame, rectcenter = templateMatching(frame)
    laserFrame, circleCentre = laserDetection(frame)
    
    print(rectcenter[0])

    # Display the resulting frame
    cv2.imshow('Frame Template Matching', templateFrame)
    cv2.imshow('Frame Laser', laserFrame)

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

  # Break the loop
  else: 
    break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()