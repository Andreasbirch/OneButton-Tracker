import os
import pandas as pd
import json
import numpy as np
from numpy.linalg import norm
from sklearn.metrics import mean_squared_error
from dtaidistance import dtw

folder_path = "../data/data"
files = [
    "02-12",
    "04-11",
    "07-10",
    "08-10",
    "09-10",
    "10-10",
    "25-11",
    "29-10"
]

def intersect(test, true):
    return len(set(true) & set(test))

def mse(test, true):
    return mean_squared_error(test, true)

def jaccard(test, true):
    return len(set(true) & set(test)) / len(set(true) | set(test))

def cosine(test, true):
    return np.dot(test, true) / (norm(test) * norm(true))

# def dtw(test, true):
#     # https://www.geeksforgeeks.org/dynamic-time-warping-dtw-in-time-series/
#     test_s = pd.Series(test).fillna(method="ffill").values
#     true_s = pd.Series(true).fillna(method="ffill").values
#     min_length = min(len(test_s), len(true_s))
#     test_s = test_s[:min_length]
#     true_s = true_s[:min_length]
#     return dtw.distance(test_s, true_s)

def binarize(df, changepoints):
    out = []
    curr_symbol = 0
    changepoints_i = 0
    for idx, row in df.iterrows():
        if changepoints_i < len(changepoints) and changepoints[changepoints_i] == idx:
            curr_symbol = 1 if curr_symbol == 0 else 0
            changepoints_i += 1
        out.append(curr_symbol)
    return out

tilt_switch_changepoints_data = {}
with open('../segmentation/tilt switches/change_points_2.json') as json_file:
    tilt_switch_changepoints_data = json.load(json_file)

scores = {}
for dataset in files:
    print(dataset)
    df = pd.read_csv(os.path.join(folder_path, "{}.csv".format(dataset)))
    stability_changepoints = []
    binarized_true = []
    curr_segment_symbol = 0

    prev = None
    # Generate breakpoints form stability classifier
    for idx, row in df.iterrows():
        binarized_true.append(curr_segment_symbol)
        if idx == 0:
            prev = row
            continue
        if row['stability'] != prev['stability']:
            stability_changepoints.append(idx)
            curr_segment_symbol = 1 if curr_segment_symbol == 0 else 0
            prev = row

    # Generate scores for each dataset, for each configuration
    scores[dataset] = {}
    configs = tilt_switch_changepoints_data[dataset].keys()
    for config in configs:
        scores[dataset][config] = {}
        ops = tilt_switch_changepoints_data[dataset][config]
        for op in ops:
            test_changepoints = tilt_switch_changepoints_data[dataset][config][op]
            test_binarized = binarize(df, test_changepoints)
            scores[dataset][config][op] = {
                'intersect': intersect(test_binarized, binarized_true),
                'mse': mse(test_binarized, binarized_true),
                'jaccard': jaccard(test_binarized, binarized_true),
                'cosine': cosine(test_binarized, binarized_true),
                # 'dtw': dtw(test_binarized, binarized_true),
            }
            print(scores[dataset][config][op])

# Write out the best performing setup for each configuration
for dataset in files:
    scores[dataset]['best'] = {}

    for k in ['intersect', 'mse', 'jaccard', 'cosine']:
        best_k = {
            'score': -1,
            'setup': {}
        }

        for config in tilt_switch_changepoints_data[dataset].keys():
            for op in tilt_switch_changepoints_data[dataset][config].keys():
                val = scores[dataset][config][op]
                if val['intersect'] > best_k['score']:
                    best_k['score'] = val['intersect']
                    best_k['setup'] = {
                        'config': config,
                        'op': op
                    }
        scores[dataset]['best'][k] = best_k

# Count number of times a specific configuration was best
possible_configurations = {
    'compare(change)': {'or': 0, 'xor': 0, 'and': 0, 'xnor': 0},
    'change(compare)': {'or': 0, 'xor': 0, 'and': 0, 'xnor': 0},
}
for dataset in files:
    for k in ['intersect', 'mse', 'jaccard', 'cosine']:
        best_setup = scores[dataset]['best'][k]['setup']
        possible_configurations[best_setup['config']][best_setup['op']] += 1
scores['best_overall'] = possible_configurations

with open('scores_2.json', 'w') as out_file:
    out_file.write(json.dumps(scores, indent=4))