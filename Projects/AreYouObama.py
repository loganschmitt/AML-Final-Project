# https://pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/

import face_recognition
import pickle
import cv2

# This script recognizes faces on an image given by the user

# Load the known faces and encodings
known_encodings = pickle.loads(open('Helper-Files/known-encodings.pickle', "rb").read())

# Process the image
# FIX: CHANGE THIS PATH TO THE IMAGE YOU WANT TO RECOGNIZE
# image = cv2.imread('Images/Obama/Obama1.png')
# image = cv2.imread('Images/You/Me.jpeg')
image = cv2.imread('Images/Unknown/Ryan-Reynolds.jpg')
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Detect the (x, y)-coordinates of the boxes around the faces in the image
boxes = face_recognition.face_locations(rgb, model = 'hog') # model can be cnn or hog
                            # cnn is better but slower, hog is faster but less accurate

# Get the encodings for the face
new_encodings = face_recognition.face_encodings(rgb, boxes)

# List of names for faces detected
new_names = []

for encoding in new_encodings:
    # Match the face with the known encodings
    matches = face_recognition.compare_faces(known_encodings["encodings"], encoding)
	# Make name unknown in case of no matches
    name = "Unknown"
    
    # Check to see if it found a match
    if True in matches:
		# find the indexes of all matched faces then initialize a
		# dictionary to count the total number of times each face
		# was matched
        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
        counts = {}
    
        # loop over the matched indexes and maintain a count for
        # each recognized face face
        for i in matchedIdxs:
            name = known_encodings["names"][i]
            counts[name] = counts.get(name, 0) + 1
    
        # determine the recognized face with the largest number of
        # votes (note: in the event of an unlikely tie Python will
        # select first entry in the dictionary)
        name = max(counts, key=counts.get)
    
# update the list of names
new_names.append(name)
print(new_names)

# Ryan Reynolds as unknown

# loop over the recognized faces
for ((top, right, bottom, left), name) in zip(boxes, new_names):
	# draw the predicted face name on the image
	cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
	y = top - 15 if top - 15 > 15 else top + 15
	cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
		0.75, (0, 255, 0), 2)

# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)