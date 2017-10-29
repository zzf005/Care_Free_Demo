from __future__ import print_function
import math
import cv2 
import numpy as np 
from imutils.object_detection import non_max_suppression
from imutils import paths

def rect_to_bb(rect):
	# take a bounding predicted by dlib and convert it
	# to the format (x, y, w, h) as we would normally do
	# with OpenCV
	x = rect.left()
	y = rect.top()
	w = rect.right() - x
	h = rect.bottom() - y
	# return a tuple of (x, y, w, h)
	return (x, y, w, h)
 
 
def shape_to_np(shape, dtype="int"):
	# initialize the list of (x, y)-coordinates
	coords = np.zeros((4, 2), dtype=dtype)
	# loop over the 68 facial landmarks and convert them
	# to a 2-tuple of (x, y)-coordinates
	for (i,j) in (36,0),(39,1),(42,2),(45,3):
		coords[j] = (shape.part(i).x, shape.part(i).y)
	# return the list of (x, y)-coordinates
	return coords

def face_extracted(img,x,y,w,h):
       my_roi = img[y:y+h , x:x+w]
       return my_roi

def img_rotation(img,degree):
    rows , cols =img.shape[:2]
    scale = 1 
    M = cv2.getRotationMatrix2D((cols/2,rows/2),degree,scale)
    res = cv2.warpAffine(img , M, (cols,rows))
    return res
       
def resized(img,size):
    if len(img)>=size[0]:
        img_resized = cv2.resize(img,(size[0],size[1]),interpolation= cv2.INTER_AREA)
    elif len(img)<size[0]:
        img_resized = cv2.resize(img,(size[0],size[1]),interpolation= cv2.INTER_CUBIC)
    return img_resized   
       
def eye_extracted(img,eyes_corner1,eyes_corner2, eyes_corner3 ,eyes_corner4 ,axesX = 19,axesY = 10):
    #measure the size of cutting & center
    
    Ylcutting_size = int(abs(eyes_corner2[0] - eyes_corner1[0]))
    Xlcutting_size = int(Ylcutting_size* 4/3)
    Yrcutting_size = int(abs(eyes_corner4[0] - eyes_corner3[0]))
    Xrcutting_size = int(Yrcutting_size* 4/3)
    
    Xcutting_size = (Xlcutting_size + Xrcutting_size) /2
    Ycutting_size = (Ylcutting_size + Yrcutting_size) /2
    
    xC,yC = int((eyes_corner1[0]+eyes_corner2[0])/2),int((eyes_corner1[1]+eyes_corner2[1])/2)
    #take the eyes out 
    eyeimg = img[int(yC-Ycutting_size*3/5):int(yC+Ycutting_size*2/5),
                 int(xC-Xcutting_size/2):int(xC+Xcutting_size/2)]
    #rotate
    y_over_x = (eyes_corner2[1]- eyes_corner1[1]) / (eyes_corner2[0] - eyes_corner1[0])
    rotate_angle = (np.arctan(y_over_x))* 180 / np.pi
    eyeimg = img_rotation(eyeimg,rotate_angle)
    #pic should reach 48,36.
    left_eye_img = resized(eyeimg,(48,36))
    left_eye_img = cornerMask_add(left_eye_img,axesX,axesY)
    
    xC,yC = int((eyes_corner3[0]+eyes_corner4[0])/2),int((eyes_corner3[1]+eyes_corner4[1])/2)
    #take the eyes out 
    eyeimg = img[int(yC-Ycutting_size*3/5):int(yC+Ycutting_size*2/5),
                 int(xC-Xcutting_size/2):int(xC+Xcutting_size/2)]
    #rotate
    y_over_x = (eyes_corner4[1]- eyes_corner3[1]) / (eyes_corner4[0] - eyes_corner3[0])
    rotate_angle = (np.arctan(y_over_x))* 180 / np.pi
    eyeimg = img_rotation(eyeimg,rotate_angle)
    #pic should reach 48,36.
    right_eye_img = resized(eyeimg,(48,36))
    right_eye_img = cornerMask_add(right_eye_img,axesX,axesY)
    eyes = np.concatenate((left_eye_img, right_eye_img),axis=1)
    return eyes
    
def cornerMask_add(img,axesX,axesY):
    (h, w) = img.shape[:2]
    (cX, cY) = (int(w * 0.5), int(h * 0.5))
    #(axesX, axesY) = abs(int(xr-xl / 2)), abs(int((yr-yl) / 2))
    ellipMask = np.zeros(img.shape[:2], dtype = "uint8")
    ellipMask[:,:]=255
    cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 3, -1)
    cornerMask = cv2.subtract(img[:,:],ellipMask)
    return cornerMask
    
def normalizeToUnit(img):
    #reshape To One Dimension
    featureVector = np.reshape(img,(1,-1))
    #normalize
    from sklearn import preprocessing
    unitVector = preprocessing.normalize(featureVector, norm='l2', axis = 1)
    return unitVector

def peopleDetction(img):
    # initialize the HOG descriptor/person detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    
    # detect people in the image
    (rects, weights) = hog.detectMultiScale(img, winStride=(4, 4),
    	padding=(8, 8), scale=1.25)
     
    # apply non-maxima suppression to the bounding boxes using a
    # fairly large overlap threshold to try to maintain overlapping
    # boxes that are still people
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])#for every human in rect
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.7)
     
    # draw the final bounding boxes
    for (xA, yA, xB, yB) in pick:
    	cv2.rectangle(img, (xA, yA), (xB, yB), (0, 255, 0), 2)
     
    # show some information on the number of bounding boxes
    print("there are " + np.str(len(pick))+ " person in this picture")
    # show the output images
    return len(pick)
    