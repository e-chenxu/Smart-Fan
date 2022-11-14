import numpy as py
import cv2
import sys
import time

#arrays and such
CFace = 0

# webcam face detection
faceCascade = cv2.CascadeClassifier(r"C:\Users\Eric\PycharmProjects\Smart-Fan\haarcascade_frontalface_default.xml")


cap = cv2.VideoCapture(0)

while True:
    # capture frame by frame
    ret, frame = cap.read()

    # find the position of the face
    face = faceCascade.detectMultiScale(
        frame,
        scaleFactor=1.3,
        minNeighbors=1,
        minSize=(40, 40),
        flags=(
                    cv2.CASCADE_DO_CANNY_PRUNING + cv2.CASCADE_FIND_BIGGEST_OBJECT + cv2.CASCADE_DO_ROUGH_SEARCH + cv2.CASCADE_SCALE_IMAGE))

    # draw the rectangle around and face find the center of the face (CFace)
    for (x, y, w, h) in face:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255))
        CFace = (w / 2 + x)

    # display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # set the value back to zero for the next pass
    CFace = 0

    #ret, frame = cap.read()

   # cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

