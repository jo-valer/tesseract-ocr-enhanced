# tesseract-ocr-enhanced
Repo for our SIV Project

## Installation
We used Python 3.12.0 and Tesseract-OCR 5.3.3. See requirements.txt for the required packages.

## Methods
The `methods` folder contains the different experiments of our project.
There are different functionalities:
- `trackbar.py`: manual or automatic tresholding
- `automatic_filtering.ipynb`: automatic filtering of the text through a specific pipeline
- `squared_paper_ocr.ipynb`: OCR on squared paper
- `squared_paper_shadow_removal.ipynb`: shadow removal on squared paper

## Results
Here are the results of all methods.
There is the `compute_metrics.py` script which automatically computes the metrics for all the methods and in `results/metrics` saves some stuff and prints on the console the average accuracy of each method.
