import socket
import datetime
import imutils
import time
import cv2
import pyautogui

def send_cmd(cmd):
	s.send(bytes(cmd, 'utf-8'))

	
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 8787
s.connect((host, port))	

status_flag = 0

# minimum area size
min_area = 5000
danger_area =30000
 
# if the video argument is None, then we are reading from webcam
camera = cv2.VideoCapture(1)
time.sleep(0.25)
 

 
# initialize 
firstFrame = None
dangerMode_switcher = "Off"

#

    
start = time.time()

time.sleep(0.5)

# loop over the frames of the video
while True:
     
    (grabbed, frame) = camera.read()
    # grab the current frame and initialize the occupied/unoccupied
    # text
    (grabbed, frame) = camera.read()
    text = "Unoccupied"
    

    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if not grabbed:
        break
    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=640)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
 
    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue

    now = time.time()
    second = now - start
    print(second)
    # refresh every 5 second
    if second % 5  <= 0.2:
        firstFrame = gray
        print("refresh")
        phoneU = imutils.resize(frame,width=240)
        cv2.imwrite("phone.jpg",phoneU)
        continue
    

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=4)
    (_,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.putText(frame, "Press 'Esc' to quit",(10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 100), 2)
    
    cv2.putText(frame, "Press 'X' to switch to DangerMode",(10, 420),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 100), 2)
    
    cv2.putText(frame, "Danger Mode is : {}".format(dangerMode_switcher),(10,440),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,  (100, 255, 100), 2)
    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < min_area:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        
        if cv2.contourArea(c) > danger_area:
            text = "Very Danger"
            cv2.putText(frame, "Room Status: {}".format(text), (10, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0,0, 255), 2)
            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10, frame.shape[0] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        if cv2.contourArea(c) <= danger_area:
            text = "Occupied"
            cv2.putText(frame, "Room Status: {}".format(text), (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)
            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

 
        
        # show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(27) & 0xFF
    dangerMode = cv2.waitKey(ord("x"))
    
    if ((text == "Unoccupied") and (status_flag == 1)):
        send_cmd("b'status_norm'")
        dangerIndex = 0
        
    if text == "Occupied":
        dangerIndex = 1
    if text == "Very Danger":
        dangerIndex = "b'status_danger'"
        send_cmd("b'status_danger'")
        status_flag = 1


    # if the `esc` key is pressed, break from the lop
    if key == 27:
        time.sleep(1)
        camera.release()
        break
    # dangerMode
    if dangerMode == ord("x"):
        time.sleep(1)
        if dangerMode_switcher == "On" :
            dangerMode_switcher = "Off"
        else :
            dangerMode_switcher = "On"
        
    if (dangerMode_switcher == "On") and (dangerIndex == "b'status_danger'") == True:
        time.sleep(0.3)
        print("switch")
        pyautogui.keyDown('winleft')
        pyautogui.press('d');
        pyautogui.keyUp('winleft')
        dangerMode_switcher = "Off"


        
        
    print(dangerMode_switcher)
        
        
        
def danger_zone(dangerIndex):
    return
        
    
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()