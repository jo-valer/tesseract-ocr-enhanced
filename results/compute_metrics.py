#!/usr/bin/python3

"""
This scripts reads the tsv files containing the results of the OCR and computes the metrics (accuracy).
"""

import os
import pandas as pd
import sys
from Levenshtein import distance

# Tsv files in the same directory as this script
DIRECTORY = os.path.dirname(os.path.realpath(__file__))
tsv_files = [f for f in os.listdir(DIRECTORY) if f.endswith('.tsv') if 'ground_truth' not in f]

print(tsv_files)

if len(tsv_files) == 0:
    print("No tsv files found in the directory of this script.")
    sys.exit(1)

for tsv_file in tsv_files:
    # Read the tsv file
    df = pd.read_csv(os.path.join(DIRECTORY, tsv_file), sep='\t')

    # Remove lines where ocr == 0
    df = df[df['ocr'] == 1]

    if "trackbar" in tsv_file:
        # Compute the distance between the ground truth and the OCR result, and the distance between the ground truth and the baseline
        df['baseline_dist'] = df.apply(lambda row: distance(row['text'], row['baseline_text']), axis=1)
        df['method_dist'] = df.apply(lambda row: distance(row['text'], row['method_text']), axis=1)

    # For each row of the dataframe, add a column computing the accuracy, defined as (u-method_dist)/u, where u is the length of the ground truth
    df['u'] = df['text'].apply(len)
    df['baseline_accuracy'] = (df['u'] - df['baseline_dist']) / df['u']
    df['method_accuracy'] = (df['u'] - df['method_dist']) / df['u']

    # Compute average accuracy for baseline and method
    avg_baseline_accuracy = df['baseline_accuracy'].mean()
    avg_method_accuracy = df['method_accuracy'].mean()
    print(f"Average baseline accuracy for {tsv_file}: {avg_baseline_accuracy:.2f}")
    print(f"Average method accuracy for {tsv_file}: {avg_method_accuracy:.2f}")

    # Save the dataframe in a subfolder
    subfolder = os.path.join(DIRECTORY, 'metrics')
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    df.to_csv(os.path.join(subfolder, tsv_file), sep='\t', index=False)
    print(f"Metrics saved in {subfolder}/{tsv_file}\n")
