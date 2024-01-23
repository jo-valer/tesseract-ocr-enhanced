#!/usr/bin/python3

"""
This is the first method for effective Text Extraction from almost all types of backgrounds: Manual Trackbar. 
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
These functions are used to create a trackbar for the image and OCR the text in the image.
"""

def nothing(x):
    pass


def manual_trackbar_ocr(image):
    if DEBUG1:
        print("DEBUG: manual_trackbar_ocr()")
        text = pytesseract.image_to_string(image, lang='eng')
        print(text)

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

        # cv2.imshow('image', image)

        # create full white image with same width of the original image and height of 20 pixels
        white_image = np.zeros((20, image.shape[1], 3), np.uint8)
        cv2.imshow('image', np.hstack([image, white_image]))

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

            # Display the resulting frame
            # cv2.imshow('image', res)
            # k = cv2.waitKey(1) & 0xFF
            # if k == 27: # wait for ESC key to exit
            #     break

            # OCR
            if (lh_i != lh) or (ls_i != ls) or (lv_i != lv) or (uh_i != uh) or (us_i != us) or (uv_i != uv):
                text = pytesseract.image_to_string(res, lang='eng')
                # print text in cv2 window
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(res, text, (10, 500), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
                # cv2.imshow('image', res)
                cv2.imshow('image', np.hstack([res, white_image]))

            k = cv2.waitKey(1) & 0xFF
            if k == 27: # wait for ESC key to exit
                break
                

        # When everything done, release the capture
        cv2.destroyAllWindows()


if __name__ == "__main__":
    #DEBUG
    PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath("FILEPATH")))
    image_path = os.path.join(PARENT_DIR, "images", "001.png")
    print(pytesseract.image_to_string(Image.open(image_path)))

    # Parent directory path
    PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if DEBUG2:
        print("DEBUG MODE: ON")
        image = cv2.imread(os.path.join(PARENT_DIR, "images", "001.png"))
    else:
        # Construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--image", required=True, help="Path to the image")
        args = vars(ap.parse_args())

        # Load the image
        image = cv2.imread(args["image"])

    # Call the function
    manual_trackbar_ocr(image)
