### This file takes in a dataset with some parameters, and generates the following data, all in a folder:
###  Data ready for plotting in observable
###  Breakpoints from tilt switches
###  Confusion matrices
###  Confusion matrix scores
from test import data

### Input goes here
FILE_PATH = "../Datasets/02-12.csv"
TRUE_WEAR_FUNC = lambda row: row['stability'] != 1
WEAR_WINDOW = 60 * 30 # more than 30 mins of no tilt = nonwear
MAX_DATA_SIZE = 10000


### Imports
import json
import pandas as pd
import datetime
import numpy as np
from collections import deque

### Read data
actual_df = pd.read_csv(FILE_PATH)
actual_df['timestamp'] = pd.to_datetime(actual_df['timestamp'], unit='s')
actual_df['acc_magnitude'] = np.sqrt(actual_df['acc_x'] ** 2 + actual_df['acc_y'] ** 2 + actual_df['acc_z'] ** 2)
actual_df['true_wear'] = actual_df.apply(TRUE_WEAR_FUNC, axis=1)


### Compute data
out_data = {
    'actual': None,
    'sim': {}
}

def simulate_data(cooldown):
    ## Simulate tilt switch deep sleep sampling
    sim_data = []
    cooldown_after_tilt = cooldown # minutes
    state = 'idle'
    cooldown_alarm = None
    woke_up_at = actual_df.iloc[0]['timestamp']
    next_tilt_from_wake_time = None
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

def generate_data(df):
    df.reset_index(inplace=True) # Reset indices
    data = {
        'breakpoints': None,
        'data': None,
        'matrices': None,
        'scores': None
    }


    ## Breakpoints
    breakpoints = []
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

            breakpoints.append(row['timestamp'])
            currentVal = row
            timeChunks.append(timeChunk)
            timeChunk = []
    # The last measurement is counted as a breakpoint regardless of value
    lastVal = df.iloc[-1]
    if breakpoints[-1] != lastVal['timestamp']:
        breakpoints.append(lastVal['timestamp'])
    # if timeChunk[-1]['timestamp'] != lastVal['timestamp']:
    #
    #     timeChunks.append(timeChunk)
    data['breakpoints'] = [str(dt) for dt in breakpoints]



    ## Data and Matrix
    _matrix = {'tn': 0, 'fp': 0, 'fn': 0, 'tp': 0}
    _data = []

    counter = 0
    for chunk in timeChunks:
        test_wear = WEAR_WINDOW > abs((chunk[0]['timestamp'] - chunk[-1]['timestamp']).total_seconds())
        # lower_bound = datetime.datetime(2024, 11, 4, 21, 24, 17)
        # upper_bound = datetime.datetime(2024, 11, 4, 22, 48, 32)

        for row in chunk:
            # true_wear = (row['timestamp'] < lower_bound) or (row['timestamp'] >= upper_bound)
            true_wear = TRUE_WEAR_FUNC(row)
            if not true_wear and not test_wear:
                _matrix['tn'] += 1
            elif not true_wear and test_wear:
                _matrix['fp'] += 1
            elif true_wear and not test_wear:
                _matrix['fn'] += 1
            elif true_wear and test_wear:
                _matrix['tp'] += 1
            if len(df) < MAX_DATA_SIZE or (counter % (len(df) // MAX_DATA_SIZE) == 0):
                _data.append({
                    'timestamp': str(row['timestamp']),
                    'wear': test_wear,
                    'stability_wear': true_wear,
                    'acc_magnitude': row['acc_magnitude'],
                })
            counter += 1

    data['data'] = _data
    data['matrices'] = _matrix

    ## Scores
    data['scores'] = {
        'accuracy': (_matrix['tn'] + _matrix['tp']) / (_matrix['tn'] + _matrix['fp'] + _matrix['tp'] + _matrix['fn']),
        'precision': (_matrix['tp']) / (_matrix['tp'] + _matrix['fp']),
        'recall': (_matrix['tp']) / (_matrix['tp'] + _matrix['fn']),
        'f1_score': 2 * ((((_matrix['tp']) / (_matrix['tp'] + _matrix['fp'])) * ((_matrix['tp']) / (_matrix['tp'] + _matrix['fn']))) / (((_matrix['tp']) / (_matrix['tp'] + _matrix['fp'])) + ((_matrix['tp']) / (_matrix['tp'] + _matrix['fn']))))
    }

    return data

## Add actual data
out_data['actual'] = generate_data(actual_df)
print("Added actual data.")

## Add simulated data
for i in range(60):
    sim_df = simulate_data(i+1)
    out_data['sim'][i] = generate_data(sim_df)
    print("Added data for cooldown length {}".format(i+1))

json.dump(out_data, open(FILE_PATH.partition('.')[0] + '_processed.json', 'w'), indent=4)
pass