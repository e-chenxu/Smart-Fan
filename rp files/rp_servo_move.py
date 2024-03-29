# Name: Eric Chen
# ID: 89351145

### import Python Modules ###
import RPi.GPIO as GPIO
import numpy as py
import cv2
import sys
import time

# arrays and such
CFace = 0

# webcam face detection
faceCascade = cv2.CascadeClassifier(r"/home/pi/Desktop/projecto/haarcascade_frontalface_default.xml")

# using board number system
GPIO.setmode(GPIO.BOARD)

# pins
LED_G = 15  # GPIO 22
SRV_P = 11  # GPIO 17

# these are converted from gpio from the lab report

GPIO.setwarnings(False)  # to disable warnings

GPIO.setup(LED_G, GPIO.OUT, initial=GPIO.LOW)  # output of greens
GPIO.setup(SRV_P, GPIO.OUT)  # output of serv

servo = GPIO.PWM(SRV_P, 50)

servo.start(7.5)
servo.ChangeDutyCycle(0)
time.sleep(2)

# arrays and such
currentPos = 7.5
max_right_p = False
max_left_p = True
minPos = 3  # This is the most left position within non-breakage range for the servo
maxPos = 11.5  # This is the most right position within non-breakage range for the servo
rangeRight = 230  # This refers the the X range for the face detection
rangeLeft = 140  # Same as reangeRight.

# If it's moving to fast and not stoping on a face mess with this variable The higher the number
# the bigger the increment it will move.
incrementServo = .15

cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)


# Functions

# Checks if the servo is in the max position to the left or right. If its not then it just
# moves the servo to the right until it's in the max right position and then moves it to the
# the max left position.
def scan():
    global currentPos
    global max_right_p
    global max_left_p

    if not max_right_pos:
        servo_right()
        if currentPos >= maxPos:
            max_right_pos = True
            max_left_pos = False
    if not max_left_pos:
        servo_left()
        if currentPos <= minPos:
            max_right_pos = False
            max_left_pos = True

        # Moves the servo to the left once. But if its already at its max left position (min_p)


# then it won't move left anymore
def servo_left():
    global currentPos
    # Checks to see if its already at the max left (min_p) posistion
    if currentPos > minPos:
        currentPos = currentPos - incrementServo
        servo.ChangeDutyCycle(currentPos)
    time.sleep(.05)  # Sleep because it reduces jitter
    servo.ChangeDutyCycle(0)  # Stop sending a signal servo also to stop jitter


# Moves the servo to the left once. But if its already at its max right position (max_p)
# then it won't move right anymore
def servo_right():
    global currentPos
    # Checks to see if its already at the max right (max_p) posistion
    if currentPos < maxPos:
        currentPos = currentPos + incrementServo
        servo.ChangeDutyCycle(currentPos)
    time.sleep(.05)  # Sleep because it reduces jitter
    servo.ChangeDutyCycle(0)  # Stop sending a signal servo also to stop jitter


# If the face is within the predetermined range don't do anything. If its outside of the range
# Adjust the servo so that the face is back in the range again. This is misleading though
# because the SERVO is turning left, however its left is our right and vice-verca.
def track_face(face_position):
    # turn the SERVO to the left (our right)
    if face_position > rangeRight:
        servo_left()

    # turn the SERVO to the right (our left)
    if face_position < rangeLeft:
        servo_right()
    time.sleep(.05)
    servo.ChangeDutyCycle(0)


def loop():
    # led
    global CFace
    GPIO.output(LED_G, GPIO.HIGH)
    while (True):

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

        # if we found a face send the position to the servo
        if CFace != 0:
            track_face(CFace)

        else:
            scan()
        # set the value back to zero for the next pass
        CFace = 0

    cap.release()
    cv2.destroyAllWindows()


# main thread
if __name__ == '__main__':
    print('Program is starting ... ')
    try:
        loop()
        GPIO.cleanup()
        exit()

    except KeyboardInterrupt:
        servo.stop()
        cap.release()
        cv2.destroyAllWindows()
        GPIO.cleanup()
        exit()



