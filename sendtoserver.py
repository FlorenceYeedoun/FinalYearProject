import cv2
import pytesseract
import requests
import json
import os
import subprocess

# Function to process the image using Tesseract OCR
def process_image(image):
    text = pytesseract.image_to_string(image)
    return text

# Set the server API endpoint
api_url = "https://traffic-offense.onrender.com/api/v1/offenses/raspberry"

# Define the violation types and their corresponding directories
violation_types = {
    "RED_LIGHT": "/home/pi/Red_Light_violation",
    "SPEEDING": "/home/pi/Speed_violation"
}
# Define the violation amounts and currency
fine = {
    "RED_LIGHT": {
        "amount": 500,
        "currency": "GHS"
    },
    "SPEEDING": {
        "amount": 320,
        "currency": "GHS"
    }
}

# Set the base directory path
base_directory = "/home/pi"

# Main loop to process images from multiple directories
for violation_type, directory_name in violation_types.items():
    directory_path = os.path.join(base_directory, directory_name)
    if not os.path.exists(directory_path):
        continue

    for file_name in os.listdir(directory_path):
        # Read the image
        image_path = os.path.join(directory_path, file_name)
        image = cv2.imread(image_path)

        # Resize the image 
        new_width = 800
        new_height = 600
        resized_image = cv2.resize(image, (new_width, new_height))

        # Process the resized image using Tesseract OCR
        text = process_image(resized_image)

        # Display the detected text and violation type
        print("Violation:", violation_type)
        print("Image:", file_name)
        print("Text:", text)
        print("----------------------")

        # Convert the image to base64 string
        _, image_encoded = cv2.imencode(".jpg", resized_image)
        image_base64 = image_encoded.tobytes()

        # Create the payload for the API request
        payload = {
            "offense_name": violation_type,
            "number_plate": text,
            "image": image_base64,
            "fine" : fine
        }

        # Send the data to the server API endpoint
        response = requests.post(api_url, json=payload)

        # Handle the response from the server
        if response.status_code == 200:
            print("Data successfully sent to the server.")
        else:
            print("Failed to send data to the server.")

        # Continue with the next image

cv2.destroyAllWindows()


