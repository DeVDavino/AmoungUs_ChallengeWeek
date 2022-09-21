import cv2
import numpy as np

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture(0)

def templateMatching(frame):
  # Load template image
  template = cv2.imread('data/red2.png',0)
  assert not isinstance(template,type(None)), 'image not found'
  w, h = template.shape[::-1]

  # Template matching method
  method = eval('cv2.TM_CCOEFF_NORMED')

  # Template matching
  frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
  frame = cv2.resize(frame, (768, 512))
  res = cv2.matchTemplate(frame,template,method)
  
  maxv = np.max(res)
  if maxv>0.80:
    # Coordinates
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    
    # Drawing bounding box and text
    cv2.rectangle(frame,top_left, bottom_right, 255, 2)
    cv2.putText(frame, 'Sus detected', (top_left[0],top_left[1]-10), 
              cv2.FONT_HERSHEY_PLAIN, 1.0, (255,255,255))

    # Getting centre of Among us
    rect1x, rect1y = ((top_left[0]+bottom_right[0])/2, (top_left[1]+bottom_right[1])/2)
    rect1center = int(rect1x),int(rect1y)
    # Show centre in frame
    cv2.circle(frame, rect1center, 20, (255,255,255), 3)

    template = frame[top_left[1]:top_left[1]+h,top_left[0]:top_left[0]+w]


# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")

# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  
  if ret == True:
    # Funcion calls here
    frame = templateMatching(frame)
     
    # Display the resulting frame
    cv2.imshow('Frame',frame)

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