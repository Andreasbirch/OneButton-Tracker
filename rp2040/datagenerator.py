### This file takes in a dataset with some parameters, and generates the following data, all in a folder:
###  Data ready for plotting in observable
###  Breakpoints from tilt switches
###  Confusion matrices
###  Confusion matrix scores
from test import data
### Imports
import json
import pandas as pd
import datetime
import numpy as np
from pathlib import Path
from collections import deque

### Input goes here
FILE_PATH = "../Datasets/simulated_device_data.csv"
TRUE_WEAR_FUNC = lambda row: row['stability'] != 1


### Read data
actual_df = pd.read_csv(FILE_PATH)
actual_df['timestamp'] = pd.to_datetime(actual_df['timestamp'], unit='s')
actual_df['true_wear'] = actual_df.apply(TRUE_WEAR_FUNC, axis=1)


### Compute data
def generate_data(_df):
    df = _df.copy()
    df.reset_index(inplace=True) # Reset indices
    ## Breakpoints
    timeChunks = []
    currentVal = df.iloc[0]
    timeChunk = []
    for index, row in df.iterrows():
        change_up = row['tilt_y'] != currentVal['tilt_y']
        change_forward = row['tilt_x'] != currentVal['tilt_x']
        timeChunk.append(row)

        if index == len(df) - 1 or (change_forward or change_up):
            if index == len(df) - 1:
                timeChunks.append(timeChunk)

            currentVal = row
            timeChunks.append(timeChunk)
            timeChunk = []

    ## Data and Matrix
    _matrix = {'tn': 0, 'fp': 0, 'fn': 0, 'tp': 0}
    _data = {'data': [],'scores': {}}

    counter = 0
    for chunk in timeChunks:
        test_wear = (60 * 60) > abs((chunk[0]['timestamp'] - chunk[-1]['timestamp']).total_seconds())

        for row in chunk:
            true_wear = TRUE_WEAR_FUNC(row)
            if not true_wear and not test_wear:
                _matrix['tn'] += 1
            elif not true_wear and test_wear:
                _matrix['fp'] += 1
            elif true_wear and not test_wear:
                _matrix['fn'] += 1
            elif true_wear and test_wear:
                _matrix['tp'] += 1
            _data['data'].append({
                'timestamp': str(row['timestamp']),
                'wear': test_wear,
                'stability_wear': true_wear,
                'acc_magnitude': row['acc_magnitude'],
            })
            counter += 1
    accuracy = (_matrix['tn'] + _matrix['tp']) / (_matrix['tn'] + _matrix['fp'] + _matrix['tp'] + _matrix['fn'])
    precision = _matrix['tp'] / (_matrix['tp'] + _matrix['fp'])
    recall = _matrix['tp'] / (_matrix['tp'] + _matrix['fn'])
    try:
        f1_score = 2 * ((precision * recall) / (precision + recall))
    except ZeroDivisionError:
        f1_score = 0

    _data['scores'] = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score
    }
    ## Scores
    return _data

out_data = generate_data(actual_df)

print("Færdig")

json.dump(out_data, open(Path(FILE_PATH).stem + '_x_y.json', 'w'), indent=4)