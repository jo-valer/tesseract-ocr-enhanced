#!/usr/bin/python3

"""
The first method for effective Text Extraction from almost all types of backgrounds is Manual Trackbar. 
The Track bar is used to apply the value for changing the 
image threshold in runtime. Creating a track bar is creating a 
progress bar for an image and adjusting various parameters. This 
track bar has six parameters: LH (Lower Hue), LS (Lower 
Saturation), LV (Lower value), UH (Upper Hue), US (Upper 
Saturation) and UV (Upper Value). This procedure helps 
us in creating a mask of a particular image and then extracting 
text from that image. This works in a precise manner for almost 
all types of background images. It improves the efficiency of 
Tesseract and thus allows us to extract text with ease and clarity.

The second method for effective Text Extraction from almost all types of backgrounds is Automatic Trackbar.
In this method, we take input from the user confirming the 
shade of the background color. Once provided with the color, it 
changes the parameters autonomously until it produces the 
desired output. This method has more probability of producing 
errors as compared to the manual method.
"""

import cv2
import numpy as np
import pytesseract
import os
import sys
import argparse
from PIL import Image

DEBUG1 = False
DEBUG2 = True
# Path to tesseract executable (in case it isn't in your PATH)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

"""
Nothing function for trackbar
"""
def nothing(x):
    pass

"""
Create manual trackbars for the image and OCR the text in the image.
"""
def manual_trackbar_ocr(image):
    if DEBUG1:
        print("DEBUG: manual_trackbar_ocr()")
        text = pytesseract.image_to_string(image, lang='eng')
        # print text in red in console
        print("\033[91m {}\033[00m" .format(text))

    else:
        cv2.namedWindow('image')
        # Create trackbars for color change
        # Hue is from 0-179 for OpenCV
        cv2.createTrackbar('LH', 'image', 0, 179, nothing)
        cv2.createTrackbar('LS', 'image', 0, 255, nothing)
        cv2.createTrackbar('LV', 'image', 0, 255, nothing)
        cv2.createTrackbar('UH', 'image', 179, 179, nothing)
        cv2.createTrackbar('US', 'image', 255, 255, nothing)
        cv2.createTrackbar('UV', 'image', 255, 255, nothing)

        # Initialize default values for color trackbars
        lh = 0
        ls = 0
        lv = 0
        uh = 179
        us = 255
        uv = 255

        cv2.imshow('image', image)

        while(1):            
            # get current positions of six trackbars
            lh_i = lh
            lh = cv2.getTrackbarPos('LH','image')
            ls_i = ls
            ls = cv2.getTrackbarPos('LS','image')
            lv_i = lv
            lv = cv2.getTrackbarPos('LV','image')
            uh_i = uh
            uh = cv2.getTrackbarPos('UH','image')
            us_i = us
            us = cv2.getTrackbarPos('US','image')
            uv_i = uv
            uv = cv2.getTrackbarPos('UV','image')

            # Convert BGR to HSV
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            # define range of blue color in HSV
            lower_blue = np.array([lh, ls, lv])
            upper_blue = np.array([uh, us, uv])

            # Threshold the HSV image to get only blue colors
            mask = cv2.inRange(hsv, lower_blue, upper_blue)

            # Bitwise-AND mask and original image
            res = cv2.bitwise_and(image, image, mask=mask)

            # OCR
            if (lh_i != lh) or (ls_i != ls) or (lv_i != lv) or (uh_i != uh) or (us_i != us) or (uv_i != uv):
                text = pytesseract.image_to_string(res, lang='eng')
                # print text in cv2 window
                # font = cv2.FONT_HERSHEY_SIMPLEX
                # cv2.putText(res, text, (10, 500), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.imshow('image', res)
                
                # print text in green in console
                print("\033[92m {}\033[00m" .format(text))  

            k = cv2.waitKey(1) & 0xFF
            if k == 27: # wait for ESC key to exit
                break
                
        cv2.destroyAllWindows()

"""
Automatically modify the values (lh, ls, lv, uh, us, uv) to OCR the text in the image.
"""
def auto_trackbar_ocr(image):

    #TODO: implement this function
    exit(0)

    # Ask user for background color
    background_color = input("Enter the background color (1 for Dark and 0 for Light, and 2 for both): ")
    if background_color == "1":
        pass
    elif background_color == "0":
        pass
    else:
        print("Invalid input!")
        sys.exit(1)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([lh, ls, lv])
    upper_blue = np.array([uh, us, uv])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(image, image, mask=mask)

    # OCR
    text = pytesseract.image_to_string(res, lang='eng')
    print("\033[92m {}\033[00m" .format(text))

# MAIN
if __name__ == "__main__":
    #DEBUG
    PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath("FILEPATH")))
    image_path = os.path.join(PARENT_DIR, "images", "001.png")
    # print text in red in console
    print("\033[91m {}\033[00m" .format(pytesseract.image_to_string(Image.open(image_path))))

    # Parent directory path
    PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if DEBUG2:
        print("DEBUG MODE: ON")
        image = cv2.imread(os.path.join(PARENT_DIR, "images", "001.png"))
    else:
        # Construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--image", required=True, help="Path to the image")
        ap.add_argument("-a", "--auto", required=False, help="Automatic Trackbar")
        args = vars(ap.parse_args())

        # Load the image
        image = cv2.imread(args["image"])

        # Depending on the argument, call the respective function
        if args["auto"] == "True":
            auto_trackbar_ocr(image)
        else:
            manual_trackbar_ocr(image)

    manual_trackbar_ocr(image)
    # auto_trackbar_ocr(image)
