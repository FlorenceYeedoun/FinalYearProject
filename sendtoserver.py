import cv2
import pytesseract
import requests
import json

# Function to process the image using Tesseract OCR
def process_image(image):
    text = pytesseract.image_to_string(image)
    return text

# Set the server API endpoint
api_url = "http://your-server.com/api/upload"

# Set the directory path to monitor
directory_path = "/path/to/pi/directory"

# Main loop to process images
for file_name in os.listdir(directory_path):
    # Read the image
    image_path = os.path.join(directory_path, file_name)
    image = cv2.imread(image_path)

    # Resize the image (if needed)
    new_width = 800
    new_height = 600
    resized_image = cv2.resize(image, (new_width, new_height))

    # Process the resized image using Tesseract OCR
    text = process_image(resized_image)

    # Display the detected text
    print("Image:", file_name)
    print("Text:", text)
    print("----------------------")

    # Convert the image to base64 string
    _, image_encoded = cv2.imencode(".jpg", resized_image)
    image_base64 = image_encoded.tobytes()

    # Create the payload for the API request
    payload = {
        "text": text,
        "image": image_base64.decode("utf-8")
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
