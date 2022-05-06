from pyimagesearch.shapedetector import ShapeDetector
import imutils
import cv2

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better

print("\n\nWould you like to see mosaic, card, or shapes/colors? \n(1 for minmals, 2 for stop_sign, 3 for shapes/colors, 0 to exit) ")
while True:
    answer = input()
    if answer == '1':
        image = cv2.imread("Images/shapes/minimal_images.jpg")
        break
    elif answer == '2':
        image = cv2.imread("Images/shapes/stop_sign.jpg")
        break
    elif answer == '3':
        image = cv2.imread("Images/shapes/shapes_and_colors.png")
        break
    elif answer == '0':
        print('Goobye!\n\n')
        break
    else:
        print("Please enter 1, 2, or 3: ")

print(f"image shape: {image.shape}")
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

print(f"ratio: {ratio}")

# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
sd = ShapeDetector()

# loop over the contours
for c in cnts:
    M = cv2.moments(c)
    cX = int((M["m10"] / M["m00"]) * ratio)
    print(f"cX:{cX}")
    cY = int((M["m01"] / M["m00"]) * ratio)
    print(f"cY:{cY}")
    shape = sd.detect(c)

    # draw the contours and the name of the shape on the image
    c = c.astype("float")
    c *= ratio
    c = c.astype("int")
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (255, 255, 255), 2)

    # show the output image
    cv2.imshow("Image", image)
    cv2.waitKey(0) # program finishes after all shapes and contours have been shown
