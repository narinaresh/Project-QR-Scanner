import keyboard
import time
import os
from pyzbar.pyzbar import decode
from PIL import Image
import cv2
import winsound
import pandas as pd
import glob


# Save local backup to Excel with multiple columns for multi-line QR data
def save_local_backup(data, excel_path="TESTING.xlsx"):
    # Split the data by line into multiple columns
    data_lines = data.splitlines()  # Each line of the QR code becomes a column
    data_dict = {
        f"Column {i+1}": [data_lines[i]] if i < len(data_lines) else [""]
        for i in range(5)
    }  # 5 columns

    if os.path.exists(excel_path):
        df_existing = pd.read_excel(excel_path)
        df_new = pd.DataFrame(data_dict)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_excel(excel_path, index=False)
    else:
        df_new = pd.DataFrame(data_dict)
        df_new.to_excel(excel_path, index=False)


# QR Code scanner main function
def qr_code_scanner(excel_path="TESING.xlsx"):
    count = 0

    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("\033[91mERROR:\033[0m Failed to open Camera!!")
        exit()

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("\033[91mERROR:\033[0m Failed to capture frame.")
                break

            # Save the captured frame temporarily
            image_path = f"cap{count}.png"
            cv2.imwrite(image_path, frame)
            if os.path.exists(image_path):
                print(f"Image saved successfully as {image_path}")
                winsound.Beep(1000, 200)

            # Decode QR code from the image
            image = Image.open(image_path)
            img_decode = decode(image)

            decoded = False
            for de_img in img_decode:
                try:
                    qr_data = de_img.data.decode("utf-8")
                    print(f"Decoded data: {qr_data}")
                    save_local_backup(
                        qr_data, excel_path
                    )  # Save local backup with multi-line support

                    decoded = True
                except UnicodeDecodeError:
                    print("\033[91mERROR:\033[0m Failed to decode QR code.")
                    winsound.Beep(1000, 2000)

            if not decoded:
                winsound.Beep(1000, 2000)

            count += 1

            # Break the loop when 'q' is pressed
            if keyboard.is_pressed("q"):
                print("Key pressed, exiting loop.")
                break

            time.sleep(1)

    finally:
        # Release camera and clean up
        cap.release()
        cv2.destroyAllWindows()

        # Delete temporary image files
        for file in glob.glob("*.png"):
            try:
                os.remove(file)
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Failed to delete {file}: {e}")


# Main execution
if __name__ == "__main__":
    qr_code_scanner()
