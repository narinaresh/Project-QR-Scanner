# This project to scan and read the formal - QR(quick response) code
# author - Naresh kumar K

# importing required libraries
import keyboard
import time
import os
from pyzbar.pyzbar import decode
from PIL import Image
import cv2
import winsound
import glob

count = 0

# Open the camera outside the loop
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("\033[91mERROR:\033[0m Failed to open Camera!!")
    exit()

try:
    while True:
        image_path = f"cap{count}.png"  # image path

        # Capture the image
        ret, frame = cap.read()

        # Check if the frame was captured
        if not ret:
            print("\033[91mERROR:\033[0m Failed to capture frame.")
            break

        # Save the image
        cv2.imwrite(image_path, frame)

        if os.path.exists(image_path):
            print(f"Image saved successfully as {image_path}")
            winsound.Beep(1000, 200)

        # Open the image
        image = Image.open(image_path)

        # Decode the image using decode function
        img_decode = decode(image)

        # Read the data inside the QR which is in the form of unicode
        decoded = False
        for de_img in img_decode:
            try:
                print(de_img.data.decode("utf-8")[0:])
                decoded = True
            except UnicodeDecodeError:
                print("\033[91mERROR:\033[0m Failed to decode QR code.")
                winsound.Beep(1000, 2000)  # Longer beep for error

        if not decoded:
            winsound.Beep(1000, 2000)  # Longer beep if no QR code found

        count += 1

        # Check if a key is pressed to exit
        if keyboard.is_pressed("q"):  # Change "q" to any key you prefer
            print("Key pressed, exiting loop.")
            break

        # Sleep for a short period to avoid excessive CPU usage
        time.sleep(1)

finally:
    # Release the camera
    cap.release()
    cv2.destroyAllWindows()

# Remove all .png files in the current directory
for file in glob.glob("*.png"):
    try:
        os.remove(file)
        print(f"Deleted: {file}")
    except Exception as e:
        print(f"Failed to delete {file}: {e}")
