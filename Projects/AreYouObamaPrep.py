DEBUG = 1
# https://pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/
# http://dlib.net/cnn_face_detector.py.html
# http://dlib.net/face_recognition.py.html

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

# TRAIN
training_folder = os.listdir('Images')
known_encodings = []
known_people = []

# Loop through each person
for folder in training_folder:
    # Loop through each training image for each person
    for file in os.listdir(f'Images/{folder}'):
        # Load the image and convert it to RGB (OpenCV uses BGR, but dlib uses RGB, and face_recognition uses dlib)
        # image = cv2.imread(f'Images/{folder}/{file}')
        image = cv2.imread('Images/'+folder+'/'+file)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # print(image)
        
        # Detect the (x, y)-coordinates of the boxes around the faces in the image
        boxes = face_recognition.face_locations(rgb, model = 'hog') # model can be cnn or hog
                                    # cnn is better but slower, hog is faster but less accurate
        
        # Get the encodings for the face
        encodings = face_recognition.face_encodings(rgb, boxes)
        
        # Add each enconding to the list of known encodings and names
        for encoding in encodings:
            known_encodings.append(encoding)
            known_people.append(folder)

# Transfer all the encodings to a file so this does not have to be done everytime
data = {"encodings": known_encodings, "names": known_people}
f = open('Helper-Files/known-encodings.pickle', "wb")
f.write(pickle.dumps(data))
f.close()


#Get the names of the image files (any file that ends with g because it may be .png or .jpg or .jpeg)
# train_images = [x for x in training_folder if x.endswith('g')]
# if DEBUG > 0: print('\n', train_images, '\n')

# # Train the model using the images and the labels
# for img in train_images:
    