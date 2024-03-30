# Enhancing Tesseract OCR
This is the repository for our _Signal, Image and Video_ course Project ([**Giovanni Valer**](https://github.com/jo-valer) and [**Laurence Bonat**](https://github.com/blauer4)).

The Report is available [here](https://github.com/jo-valer/tesseract-ocr-enhanced/blob/main/SIV_Report_Valer_Bonat.pdf).

## Installation
We used Python 3.12.0 and Tesseract-OCR 5.3.3. See <a href="https://github.com/jo-valer/tesseract-ocr-enhanced/blob/main/requirements.txt">requirements.txt</a> for the required packages.

## Methods
The `methods` folder contains the different experiments of our project.
There are different functionalities:
- `manual_trackbar.py`: trackbar in manual mode
- `autonomous_trackbar.ipynb`: trackbar in autonomous mode
- `automatic_filtering.ipynb`: automatic filtering of the text through a specific pipeline
- `lines_detection.ipynb`: automatically detect if a text is on lined/squared paper
- `squared_paper_ocr.ipynb`: HTR on lined/squared paper

## Results
In `results` are the results of all methods.
There is the `compute_metrics.py` script which automatically computes and saves the average accuracy of each method in `results/results.txt`, (plus some other metrics in `results/metrics`).
