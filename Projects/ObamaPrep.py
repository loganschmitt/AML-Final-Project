# Code for this project was inspired by the following tutorial:
# https://pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/


# https://learnopencv.com/deep-learning-with-opencvs-dnn-module-a-definitive-guide/#guide-to-image-classification
# https://stackoverflow.com/questions/37215036/dlib-vs-opencv-which-one-to-use-when
    # Wanted to use DNN Module from Open CV bc it is the best out there, but it only works with pre-trained models. 
    # It does not support training. So we are using dlib
    # http://dlib.net/

# Wanted to use dlib, but all examples I found online use face_recognition. So we are using that because 
# I can understand how it works. face_recognition wraps around dlib and makes it easier to use. Also need opencv installed.
# Needs new package called imutils to work with images. Apparently, the model is already trained.
# https://github.com/ageitgey/face_recognition
# https://pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
    # Look at encode_faces.py and recognize_faces_video.py
    # Uses a pre-trained network to get a 128D enconding of the faces. Then use a KNN-Model to make the face classification.
    # Let's use another model to recognize faces.

import cv2
import os
import face_recognition
import pickle
import time

start = time.time()

# Get Obama's face encodings
training_folder = os.listdir('Images/Obama')
known_encodings = []
known_people = []

# Loop through each training image for Obama
for file in os.listdir('Images/Obama'):
    # Load the image and convert it to RGB 
    # (OpenCV uses BGR, but dlib uses RGB, and face_recognition uses dlib)
    image = cv2.imread(f'Images/Obama/{file}')
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Detect the (x, y)-coordinates of the boxes around the faces in the image
    boxes = face_recognition.face_locations(rgb, model = 'cnn') # model can be cnn or hog
                                # cnn is better but slower, hog is faster but less accurate

    # Get the encodings for the face
    encodings = face_recognition.face_encodings(rgb, boxes)
    
    # Add each enconding to the list of known encodings and names
    for encoding in encodings:
        known_encodings.append(encoding)
        known_people.append('Obama')

# Transfer all the encodings to a file so this does not have to be done everytime
data = {"encodings": known_encodings, "names": known_people}
f = open('Helper-Files/Obama-encodings.pickle', "wb")
f.write(pickle.dumps(data))
f.close()

end = time.time()
print(f'Time to get Obama\'s encodings: {end - start}')

# Times for 2 Obama pictures
# CNN TIME: 189.45 seconds / ~3:10 minutes
# HOG TIME: 1.5 seconds / ~0:05 minutes