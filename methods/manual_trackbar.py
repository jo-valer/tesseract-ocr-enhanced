#!/usr/bin/python3

"""
The first method for effective Text Extraction is Manual Trackbar. 
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
import argparse
import subprocess
import sys

GREYSCALE = False

# Path to tesseract executable (in case it isn't in your PATH)
try:
    subprocess.call(["tesseract"])
except FileNotFoundError:
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
    print("Text before filtering: ")
    print("\033[91m {}\033[00m".format(pytesseract.image_to_string(image)))

    cv2.namedWindow('image')
    # Create trackbars for color change
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

    while (1):
        # get current positions of six trackbars
        lh_i = lh
        lh = cv2.getTrackbarPos('LH', 'image')
        ls_i = ls
        ls = cv2.getTrackbarPos('LS', 'image')
        lv_i = lv
        lv = cv2.getTrackbarPos('LV', 'image')
        uh_i = uh
        uh = cv2.getTrackbarPos('UH', 'image')
        us_i = us
        us = cv2.getTrackbarPos('US', 'image')
        uv_i = uv
        uv = cv2.getTrackbarPos('UV', 'image')

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define ranges in HSV
        lower_bound = np.array([lh, ls, lv])
        upper_bound = np.array([uh, us, uv])

        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        res = cv2.bitwise_and(image, image, mask=mask)

        # OCR
        if (lh_i != lh) or (ls_i != ls) or (lv_i != lv) or (uh_i != uh) or (us_i != us) or (uv_i != uv):
            if GREYSCALE:
                text = pytesseract.image_to_string(cv2.cvtColor(res, cv2.COLOR_BGR2GRAY))
            else:
                text = pytesseract.image_to_string(res)

            cv2.imshow('image', res)

            print("Text after filtering: ")
            print("\033[92m {}\033[00m".format(text))

        k = cv2.waitKey(1) & 0xFF
        if k == 27:  # wait for ESC key to exit
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath("FILEPATH")))
    image_path = os.path.join(PARENT_DIR, "images", "001.jpg")
    image = cv2.imread(image_path)
    manual_trackbar_ocr(image)
