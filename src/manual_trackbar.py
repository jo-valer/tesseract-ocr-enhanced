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
# import sys
import argparse

DEBUG = True

"""
This function is used to create a trackbar for the image and OCR the text in the image.
"""
def manual_trackbar_ocr(image):
    if DEBUG:
        print("DEBUG: manual_trackbar_ocr()")
        text = pytesseract.image_to_string(image, lang='eng')
        print(text)

    else:
        # Create a window
        cv2.namedWindow('image')

        # Create trackbars for color change
        # Hue is from 0-179 for Opencv
        cv2.createTrackbar('LH', 'image', 0, 179, nothing)
        cv2.createTrackbar('LS', 'image', 0, 255, nothing)
        cv2.createTrackbar('LV', 'image', 0, 255, nothing)
        cv2.createTrackbar('UH', 'image', 179, 179, nothing)
        cv2.createTrackbar('US', 'image', 255, 255, nothing)
        cv2.createTrackbar('UV', 'image', 255, 255, nothing)

        while(1):
            # Get the current positions of four trackbars
            lh = cv2.getTrackbarPos('LH', 'image')
            ls = cv2.getTrackbarPos('LS', 'image')
            lv = cv2.getTrackbarPos('LV', 'image')
            uh = cv2.getTrackbarPos('UH', 'image')
            us = cv2.getTrackbarPos('US', 'image')
            uv = cv2.getTrackbarPos('UV', 'image')

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
            cv2.imshow('image', res)
            k = cv2.waitKey(1) & 0xFF
            if k == 27: # wait for ESC key to exit
                break

            # OCR
            text = pytesseract.image_to_string(res, lang='eng')
            print(text)

        # When everything done, release the capture
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # Parent directory path
    PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if DEBUG:
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
