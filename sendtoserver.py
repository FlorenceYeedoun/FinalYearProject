import os
import base64
import requests
import json

# Set the server API endpoint
api_url = "https://traffic-offense.onrender.com/api/v1/offenses/raspberry"

# Define the violation types and their corresponding directories
violation_types = {
    "RED_LIGHT": "/home/flo/Red_Light_violation",
    "SPEEDING": "/home/flo/Speed_violation"
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
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        # Convert the image to base64 string
        image_base64 = base64.b64encode(image_data).decode('utf-8')

        # Create the payload for the API request
        payload = {
            "offense_name": violation_type,
            "image": image_base64,
            "file_name": file_name,
            "fine": {
                "amount": fine[violation_type]["amount"],
                "currency": fine[violation_type]["currency"]
            }
        }

        # Print the payload
        print("Payload:")
        print(json.dumps(payload, indent=4))

        # Save a copy of the image locally with the original file name
        image_copy_path = os.path.join(base_directory, file_name)
        with open(image_copy_path, 'wb') as image_copy_file:
            image_copy_file.write(image_data)

        # Send the data to the server API endpoint
        response = requests.post(api_url, json=payload)

        # Handle the response from the server
        if response.status_code == 200:
            print("Data successfully sent to the server.")
        else:
            print("Failed to send data to the server.")
            print("Response content:", response.content.decode())

        # Continue with the next image
