import RPi.GPIO as GPIO
import time 
import os
from picamera import PiCamera
import subprocess

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)
red_pin = 17
yellow_pin = 27
green_pin = 22
trig_pin = 23
echo_pin = 13
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(yellow_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

# Define a function to measure the distance
def measure_distance():
    # Send a pulse to the TRIG pin
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig_pin, GPIO.LOW)

    # Wait for the ECHO pin to go high
    pulse_start = time.time()
    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()

    # Wait for the ECHO pin to go low
    pulse_end = time.time()
    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()

    # Calculate the distance based on the pulse duration
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

# Main loop
while True:

    # Red light
    GPIO.output(red_pin, GPIO.HIGH)
    GPIO.output(yellow_pin, GPIO.LOW)
    GPIO.output(green_pin, GPIO.LOW)
    time.sleep(10)

    # Check for nearby objects
    distance = measure_distance()
    print("The distance is:",distance)
    if distance <= 10:
        # Capture images
        for i in range(7):
            os.system("raspistill -o /home/pi/Pictures/image{}.jpg".format(i))
            time.sleep(0.5)

    # Yellow light
    GPIO.output(red_pin, GPIO.LOW)
    GPIO.output(yellow_pin, GPIO.HIGH)
    GPIO.output(green_pin, GPIO.LOW)
    time.sleep(5)

    # Green light
    GPIO.output(red_pin, GPIO.LOW)
    GPIO.output(yellow_pin, GPIO.LOW)
    GPIO.output(green_pin, GPIO.HIGH)
    time.sleep(7)

    
    # Clean up the GPIO pins when the program is finished
    GPIO.cleanup()
