import cv2
import pytesseract
import os

# Function to process the image using Tesseract OCR
def process_image(image):
    text = pytesseract.image_to_string(image)
    return text

# # Set the directory paths to monitor
# directory_paths = ["/path/to/directory1", "/path/to/directory2"]
# 

# Set the directory path to monitor
directory_path = "/home/pi/Red_Light_violation"

# Main loop to process images
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

    # Display the detected text
    print("Image:", file_name)
    print("Text:", text)
    print("----------------------")

    # Display the resized image
    cv2.imshow("Resized Image", resized_image)
    cv2.waitKey(0)

cv2.destroyAllWindows()









