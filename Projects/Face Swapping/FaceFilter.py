import cv2
import dlib
import numpy as np
import math

landmark_detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

img = cv2.imread("Images/Your-Pictures/wyatt_pic.jpg")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
mask = np.zeros_like(img_gray)

img_filter = cv2.imread('Images/FaceFilters/dog-filter-transparent-background-15.png')

vid_capture=cv2.VideoCapture(0)
vid, frame = vid_capture.read()
rows, cols, _vid= frame.shape
dog_mask = np.zeros((rows, cols))

landmarks = landmark_predictor(img_gray, face)

nosetop = (landmarks.part(27).x, landmarks.part(27).y)
nosemid = (landmarks.part(30).x, landmarks.part(30).y)
noseleft = (landmarks.part(31).x, landmarks.part(31).y)
noseright = (landmarks.part(35).x, landmarks.part(35).y)