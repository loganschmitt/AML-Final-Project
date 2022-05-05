# Code for this project was inspired by the following tutorial:
# https://pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/

import face_recognition
import pickle
import cv2
import os
import LiveObama as lo

# This script recognizes faces on the images given by the user

def find_obama(file, known_encodings):
    # List of names for faces detected
    new_names = []

    # Load the image and convert it to RGB (OpenCV uses BGR, but dlib uses RGB, and face_recognition uses dlib)
    # image = cv2.imread('Images/Unknown/'+file)
    image = cv2.imread('Images/Your-Pictures/'+file)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Detect the (x, y)-coordinates of the boxes around the faces in the image
    boxes = face_recognition.face_locations(rgb, model = 'hog') # model can be cnn or hog
                                # cnn is better but slower, hog is faster but less accurate
                                
    # Get the encodings for the faces found in the image
    new_encodings = (face_recognition.face_encodings(rgb, boxes))

    for encoding in new_encodings:
        
        # Match the faces found in the image with the known encodings
        matches = face_recognition.compare_faces(known_encodings["encodings"], encoding)
            # Compares the faces in the image to the ones that have already been processed in the pickle file
            # Returns True if a match is found

        # Choose name in case it is not President Barack Obama
        name = "Not Obama"
        
        # Check for matches
        if True in matches:
            # Find the index of the matched faces, then create a dictionary
            # to count the total number of times each face was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
        
            # Loop over the matched faces and count each recognized face
            for i in matchedIdxs:
                name = known_encodings["names"][i]
                counts[name] = counts.get(name, 0) + 1
        
            # Determine whose face it is by finding the largest count (votes)
            # In case of tie, choose the first one
            name = max(counts, key=counts.get)

        # Update the list of names
        new_names.append(name)

    # Loop over the faces found
    for ((top, right, bottom, left), name) in zip(boxes, new_names):
        # Draw the face and name on the image
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
            0.75, (0, 255, 0), 2)
    
    # Show the picture
    cv2.imshow("Image", image)
    cv2.waitKey(0)  # Wait for any key to be pressed (so we can see the next image)

# Load the known faces and encodings into a dictionary
    # Keys: 'encodings' and 'names'
    # known_encodings['names'] to return the names
    

print("\n\nWould you like to detect President Barack Obama on a picture uploaded by you or on live camera? \n(1 for uploaded, 2 for live, 0 to exit) ")

while True:
    answer = input()
    if answer == '1':
        known_encodings = pickle.loads(open('Helper-Files/Obama-encodings.pickle', "rb").read())


        # source_folder = os.listdir('Images/Unknown')
        source_folder = os.listdir('Images/Your-Pictures')

        for file in source_folder:
            find_obama(file, known_encodings)
        
    elif answer == '2':
        lo.runLiveObama()

    elif answer == '0':
        print('Goobye!\n\n')
        break
    else:
        print("Please enter 1 or 2: ")