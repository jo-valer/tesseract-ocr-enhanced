# tesseract-ocr-enhanced
Repo for our SIV Project (Giovanni Valer and Laurence Bonat).

## Installation
We used Python 3.12.0 and Tesseract-OCR 5.3.3. See requirements.txt for the required packages.

## Methods
The `methods` folder contains the different experiments of our project.
There are different functionalities:
- `manual_trackbar.py`: manual tresholding
- `autonomous_trackbar.ipynb`: autonomous tresholding
- `automatic_filtering.ipynb`: automatic filtering of the text through a specific pipeline
- `squared_paper_ocr.ipynb`: OCR on lined/squared paper
- `lines_detection.ipynb`: methods to automatically detect if an image is a lined/squared paper

## Results
In `results` are the results of all methods.
There is the `compute_metrics.py` script which automatically computes and saves the average accuracy of each method in `results/results.txt`, (plus some other metrics in `results/metrics`).
