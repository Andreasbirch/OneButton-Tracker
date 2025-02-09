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
FILE_PATH = "../Datasets/03-12.csv"
TRUE_WEAR_FUNC = lambda row: row['stability'] != 1


### Read data
actual_df = pd.read_csv(FILE_PATH)
actual_df['timestamp'] = pd.to_datetime(actual_df['timestamp'], unit='s')
actual_df['acc_magnitude'] = np.sqrt(actual_df['acc_x'] ** 2 + actual_df['acc_y'] ** 2 + actual_df['acc_z'] ** 2)
actual_df['true_wear'] = actual_df.apply(TRUE_WEAR_FUNC, axis=1)


### Compute data
out_data = dict({'cooldown': {}})

def simulate_data(cooldown):
    ## Simulate tilt switch deep sleep sampling
    sim_data = []
    cooldown_after_tilt = cooldown # minutes
    state = 'idle'
    cooldown_alarm = None
    # A tilt switch change is detected
    # Wake up, log sensors
    # Set a cooldown timer for n minutes, sleep
    # Wake up, log sensors
    # Listen for next tilt switch change

    _currentVal = actual_df.iloc[0]
    for index, row in actual_df.iterrows():
        if state == 'idle':
            # Get next tilt from wake time
            change_up = row['tilt_up'] != _currentVal['tilt_up']
            change_forward = row['tilt_forward'] != _currentVal['tilt_forward']
            if index == len(actual_df) - 1 or (change_up or change_forward):
                sim_data.append(row)

                # Set alarm and change state
                cooldown_alarm = row['timestamp'] + datetime.timedelta(minutes=cooldown_after_tilt)
                _currentVal = row
                state = 'cooldown'

        elif state == 'cooldown':
            if row['timestamp'] > cooldown_alarm:
                sim_data.append(row)

                woke_up_at = row['timestamp']
                state = 'idle'

    # The last measurement is counted as a breakpoint regardless of value
    if sim_data[-1]['timestamp'] != actual_df.iloc[-1]['timestamp']:
        sim_data.append(actual_df.iloc[-1])
    return pd.DataFrame(sim_data, columns=actual_df.columns)

def generate_data(_df, window_size):
    df = _df.copy()
    df.reset_index(inplace=True) # Reset indices
    ## Breakpoints
    timeChunks = []
    currentVal = df.iloc[0]
    timeChunk = []
    for index, row in df.iterrows():
        change_up = row['tilt_up'] != currentVal['tilt_up']
        change_forward = row['tilt_forward'] != currentVal['tilt_forward']
        timeChunk.append(row)

        if index == len(df) - 1 or (change_forward or change_up):
            if index == len(df) - 1:
                timeChunks.append(timeChunk)

            currentVal = row
            timeChunks.append(timeChunk)
            timeChunk = []

    ## Data and Matrix
    _matrix = {'tn': 0, 'fp': 0, 'fn': 0, 'tp': 0}

    counter = 0
    for chunk in timeChunks:
        test_wear = (window_size * 60) > abs((chunk[0]['timestamp'] - chunk[-1]['timestamp']).total_seconds())

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
            counter += 1
    accuracy = (_matrix['tn'] + _matrix['tp']) / (_matrix['tn'] + _matrix['fp'] + _matrix['tp'] + _matrix['fn'])
    precision = _matrix['tp'] / (_matrix['tp'] + _matrix['fp'])
    recall = _matrix['tp'] / (_matrix['tp'] + _matrix['fn'])
    try:
        f1_score = 2 * ((precision * recall) / (precision + recall))
    except ZeroDivisionError:
        f1_score = 0

    ## Scores
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score
    }


for i in range(1, 61):
    sim_df = simulate_data(i)
    print("Cooldown length {}".format(i))
    out_data['cooldown'][i] = {'window': {}}
    for window in range(1, 61):
        out_data['cooldown'][i]['window'][window] = generate_data(sim_df, window)
print("Færdig")

json.dump(out_data, open(Path(FILE_PATH).stem + '_x_y.json', 'w'), indent=4)