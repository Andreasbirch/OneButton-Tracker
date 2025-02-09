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

### Read data
actual_df = pd.read_csv(FILE_PATH)
actual_df['timestamp'] = pd.to_datetime(actual_df['timestamp'])

### Compute data
def generate_wear_data(_df):
    df = _df.copy()
    df = df.loc[df['reason'] == 0]

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
    _data = []

    counter = 0
    for chunk in timeChunks:
        test_wear = (60 * 60) > abs((chunk[0]['timestamp'] - chunk[-1]['timestamp']).total_seconds())

        for row in chunk:
            _data.append({
                'timestamp': str(row['timestamp']),
                'wear': test_wear,
                'acc_magnitude': row['acc_magnitude'],
            })
            counter += 1
    return _data

def generate_presses_data(_df):
    df = _df.copy()
    df = df.loc[df['reason'] == 1]
    df.reset_index(inplace=True) # Reset indices
    return df.filter(['timestamp', 'duration'], axis=1).to_dict(orient='records')

def generate_timechunk_data(_df):
    _df = pd.DataFrame(generate_wear_data(_df))
    _df['timestamp'] = pd.to_datetime(_df['timestamp'])
    periods = []
    start = _df.loc[0, 'timestamp']
    current_value = _df.loc[0, 'wear']

    for i in range(1, len(_df)):
        if _df.loc[i, 'wear'] != current_value:
            # Close the current group and start a new one
            periods.append({
                'start': start,
                'end': _df.loc[i - 1, 'timestamp'],
                'value': current_value
            })
            # Start a new group
            start = _df.loc[i, 'timestamp']
            current_value = _df.loc[i, 'wear']

    # Add the final group
    periods.append({
        'start': start,
        'end': _df.loc[len(_df) - 1, 'timestamp'],
        'value': current_value
    })

    return periods



#json.dump(generate_wear_data(actual_df), open(Path(FILE_PATH).stem + '_wear.json', 'w'), indent=4)
#json.dump(generate_presses_data(actual_df), open(Path(FILE_PATH).stem + '_presses.json', 'w'), indent=4, default=str)
json.dump(generate_timechunk_data(actual_df), open(Path(FILE_PATH).stem + '_timechunks.json', 'w'), indent=4, default=str)
print("Færdig")
