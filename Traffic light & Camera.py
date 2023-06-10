import RPi.GPIO as GPIO
import time 
import os
from picamera import PiCamera
import subprocess

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
red_pin = 22
yellow_pin = 27
green_pin = 17
trig_pin = 23
echo_pin = 13
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(yellow_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

RED_TIME = 10
YELLOW_TIME = 5
GREEN_TIME = 7

active_light = "red"
time_active = RED_TIME

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

def switch_light(light):
    if light == "red":
        GPIO.output(red_pin, GPIO.HIGH)
        GPIO.output(yellow_pin, GPIO.LOW)
        GPIO.output(green_pin, GPIO.LOW)
    elif light == "yellow":
        GPIO.output(red_pin, GPIO.LOW)
        GPIO.output(yellow_pin, GPIO.HIGH)
        GPIO.output(green_pin, GPIO.LOW)
    else:
        GPIO.output(red_pin, GPIO.LOW)
        GPIO.output(yellow_pin, GPIO.LOW)
        GPIO.output(green_pin, GPIO.HIGH)
    

start_time = time.time()
switch_light(active_light)
# Main loop
while True:
    print(active_light)
    # Red light
    if active_light == "red":
#         print(time.time() - start_time)
        
        # Check for nearby objects
        distance = measure_distance()
        print("The distance is:",distance)
        if distance <= 10:
            # Capture images
#             for i in range(7):
            obj = time.strftime("%y%m%d%H%M%S", time.gmtime(time.time()))
            os.system("raspistill -o /home/flo/Red_Light_violation/image{}.jpg -vf -hf".format(obj))
            time.sleep(0.5)
            
        if time.time() - start_time >= time_active:
            start_time = time.time()
            active_light = "yellow"
            time_active = YELLOW_TIME
            switch_light(active_light)
            
    # Yellow light
    if active_light == "yellow":
        if time.time() - start_time >= time_active:
            start_time = time.time()
            active_light = "green"
            time_active = GREEN_TIME
            switch_light(active_light)
        
    # Green light
    if active_light == "green":
        if time.time() - start_time >= time_active:
            start_time = time.time()
            active_light = "red"
            time_active = GREEN_TIME
            switch_light(active_light)

    
# Clean up the GPIO pins when the program is finished
GPIO.cleanup()
