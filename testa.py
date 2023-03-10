# Created by: Michael Klements
# For 40mm 5V PWM Fan Control On A Raspberry Pi
# Sets fan speed proportional to CPU temperature - best for good quality fans
# Works well with a Pi Desktop Case with OLED Stats Display
# Installation & Setup Instructions - https://www.the-diy-life.com/connecting-a-pwm-fan-to-a-raspberry-pi/

import RPi.GPIO as IO          # Calling GPIO to allow use of the GPIO pins
import time                    # Calling time to allow delays to be used
import subprocess              # Calling subprocess to get the CPU temperature

IO.setwarnings(False)          # Do not show any GPIO warnings
IO.setmode (IO.BOARD)            # BCM pin numbers - PIN8 as ‘GPIO14’
IO.setup(12,IO.OUT)            # Initialize GPIO14 as our fan output pin
fan = IO.PWM(12,100)           # Set GPIO14 as a PWM output, with 100Hz frequency (this should match your fans specified PWM frequency)
fan.start(0)                   # Generate a PWM signal with a 0% duty cycle (fan off)

minTemp = 25                   # Temperature and speed range variables, edit these to adjust max and min temperatures and speeds
maxTemp = 80
minSpeed = 0
maxSpeed = 100

while 1:                                    # Execute loop forever
    
    
    for i in range(0,100,10):
        fan.ChangeDutyCycle(i)
        print(i)# Set fan duty based on temperature, from minSpeed to maxSpeed
        time.sleep(1)                           # Sleep for 5 seconds