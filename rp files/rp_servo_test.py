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

cap = cv2.VideoCapture(0)

# using board number system
GPIO.setmode(GPIO.BOARD)

# pins
LED_G = 15  # GPIO 22
SRV_P = 11  # GPIO 17

# these are converted from gpio from the lab report

GPIO.setwarnings(False)  # to disable warnings

GPIO.setup(LED_G, GPIO.OUT, initial=GPIO.LOW)  # output of greens
GPIO.setup(SRV_P, GPIO.OUT)  # output of serv

pwm = GPIO.PWM(SRV_P, 50)

pwm.start(0)
time.sleep(2)


def loop():
    # led
    GPIO.output(LED_G, GPIO.HIGH)

    # Define variable duty
    duty = 2

    # Loop for duty values from 2 to 12 (0 to 180 degrees)
    while duty <= 12:
        pwm.ChangeDutyCycle(duty)
        time.sleep(0.3)
        pwm.ChangeDutyCycle(0)
        time.sleep(0.7)
        duty = duty + 1

    # Wait a couple of seconds
    time.sleep(2)

    # Turn back to 90 degrees
    print("Turning back to 90 degrees for 2 seconds")
    pwm.ChangeDutyCycle(7)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)
    time.sleep(1.5)

    # turn back to 0 degrees
    print("Turning back to 0 degrees")
    pwm.ChangeDutyCycle(2)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)
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
        pwm.stop()
        cap.release()
        cv2.destroyAllWindows()
        GPIO.cleanup()
        exit()



