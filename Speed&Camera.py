import RPi.GPIO as GPIO
import time
import picamera
import os
# from picamera import PiCamera
# import subprocess


# Set up GPIO pins for the ultrasonic sensor
GPIO.setmode(GPIO.BCM)
TRIG_PIN1 = 23
ECHO_PIN1 = 13

TRIG_PIN2 = 24
ECHO_PIN2 = 12

GPIO.setup(TRIG_PIN1, GPIO.OUT)
GPIO.setup(ECHO_PIN1, GPIO.IN)

GPIO.setup(TRIG_PIN2, GPIO.OUT)
GPIO.setup(ECHO_PIN2, GPIO.IN)

CAR_PASSED = False

START_TIME =  0
END_TIME = 0

# distance between sensors in cm
DISTANCE = 26

# Camera initialization
camera = picamera.PiCamera()

# Define a function to measure the distance to an object in front of the sensor
def measure_distance(TRIG_PIN, ECHO_PIN):
    # Send a pulse on the TRIG_PIN to trigger the ultrasonic sensor
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)
    
    # Wait for the ECHO_PIN to go high and then low
    pulse_start = time.time()
    
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        pulse_start = time.time()
    
    pulse_end = time.time()
    
    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        pulse_end = time.time()
    # Calculate the distance based on the duration of the pulse
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    
    return distance
    
    
def car_passed(TRIG_PIN, ECHO_PIN):
    if measure_distance(TRIG_PIN, ECHO_PIN) <= 7:
        print("car passed")
        return True
    
    
def get_speed():
    global START_TIME, DISTANCE
    if car_passed(TRIG_PIN1, ECHO_PIN1):
        START_TIME = time.time()
        CAR_PASSED = True
    if car_passed(TRIG_PIN2, ECHO_PIN2):
        END_TIME = time.time()
        CAR_PASSED = False
        return DISTANCE / (END_TIME - START_TIME)
        
def passed_speed(speed):
    if speed > 5:
        return True

# Main program loop
while True:
    
    GPIO.setup(TRIG_PIN1, GPIO.OUT)
    GPIO.setup(ECHO_PIN1, GPIO.IN)
    
    GPIO.setup(TRIG_PIN2, GPIO.OUT)
    GPIO.setup(ECHO_PIN2, GPIO.IN)

    speed = get_speed()
    if speed:
        print(f"Speed of car: {round(speed, 2)} cm/s \n")
        if passed_speed(speed):
            print("Ha!")
            
            # Set the camera resolution
            camera.resolution = (640, 480)
            obj = time.strftime("%y%m%d%H%M%S", time.gmtime(time.time()))
            # Capture the photo and save it to a file
            camera.capture(obj +'.jpg')


     # Capture images
           # for i in range(7):
            #    os.system("raspistill -o /home/pi/Pictures/image{}.jpg".format(i))
             #   time.sleep(0.5)
              
    else:
        print(speed)
    # Wait for a short period before measuring the distance again
    time.sleep(1)
               

# Clean up GPIO resources
GPIO.cleanup()

