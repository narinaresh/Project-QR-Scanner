# Project QR (quick response) scanner

from pyzbar.pyzbar import decode #Importing decode function to decode the QR code
from PIL import Image #Importing Image function to open the image 
import cv2

# opening a image 
img_path = "detaills.png"
image = Image.open(img_path)

#decoding the image using decode function
img_decode = decode(image)

# reading the data inside the QR which in the form of utf-8 encoding and decoding format
for de_img in img_decode:
    print(de_img.data.decode("utf-8")[0:])

print(cv2.__version__)