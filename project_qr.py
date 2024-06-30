# Project QR (quick response) scanner
# importing required libraries

import keyboard
import time
import os
from pyzbar.pyzbar import decode
from PIL import Image
import cv2
import winsound

count = 0

while(1):

    cap = cv2.VideoCapture(0)
    
    # check camera opening
    if not cap.isOpened():
        print("\033[91mERROR:\033[0m Failed to open Camera!!")
        exit()

    image_path = f"cap{count}.png"  # image path

    # capture the image
    ret, frame = cap.read()

    # check it's captured
    if not ret:
        print("\033[91mERROR:\033[0m Failed to capture frame.")
        exit()
        
    # saving the image
    cv2.imwrite(image_path, frame)

    if os.path.exists(image_path):
        print(f"Image saved successfully as {image_path}")
        winsound.Beep(1000, 200)

    # opening a image
    image = Image.open(image_path)

    # decoding the image using decode function
    img_decode = decode(image)

    # reading the data inside the QR which is in the form unicode
    for de_img in img_decode:
        print(de_img.data.decode("utf-8")[0:])

    count = count + 1

cap.release()