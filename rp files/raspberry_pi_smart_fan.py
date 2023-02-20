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

# sleep to allow servo to get time
time.sleep(2)

# initial positions
currentPos = 7.5
max_right_p = False
max_left_p = True


min_p = 3                # max left position of servo
max_p = 11.5             # max right positioon of servo
scan_range_right = 230   # max right scan
scan_range_left = 140    # max left scan

increment = .15

# setting up webcam
cap = cv2.VideoCapture(0)
cap.set(3, 320)  # width
cap.set(4, 240)  # height


# function will scan for a face if nothing in view
def scan_face():
    global currentPos
    global max_right_p
    global max_left_p

    if not max_right_p:
        servo_right()
        if currentPos >= max_p:
            max_right_p = True
            max_left_p = False

    if not max_left_p:
        servo_left()
        if currentPos <= min_p:
            max_right_p = False
            max_left_p = True


# move left
def servo_left():
    global currentPos

    # move left if not at minimum position
    if currentPos > min_p:
        currentPos = currentPos - increment
        servo.ChangeDutyCycle(currentPos)

    # jitter problems
    time.sleep(.05)
    servo.ChangeDutyCycle(0)


# move right
def servo_right():
    global currentPos

    # move right if not at maximum position
    if currentPos < max_p:
        currentPos = currentPos + increment
        servo.ChangeDutyCycle(currentPos)

    # jitter problems
    time.sleep(.05)
    servo.ChangeDutyCycle(0)


# track the face while it is moving
def track_face(face_position):
    # servo to the left (our right)
    if face_position > scan_range_right:
        servo_left()

    # servo to the right (our left)
    if face_position < scan_range_left:
        servo_right()

    # jitter problems
    time.sleep(.05)
    servo.ChangeDutyCycle(0)


def loop():
    global CFace
    # led
    GPIO.output(LED_G, GPIO.HIGH)
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

        # if we found a face send the position to the servo
        if CFace != 0:
            track_face(CFace)

        else:
            test = 0
            scan_face()
        # set the value back to zero for the next pass
        CFace = 0

    cap.release()
    cv2.destroyAllWindows()


# main thread
if __name__ == '__main__':
    print('Program is starting ... ')
    try:
        loop()
        servo.stop()
        GPIO.cleanup()
        exit()

    except KeyboardInterrupt:
        servo.stop()
        cap.release()
        cv2.destroyAllWindows()
        GPIO.cleanup()
        exit()


