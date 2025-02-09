import os
import pandas as pd
import json
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

# def mse(test, true):
#     return mean_squared_error(test, true)

def jaccard(test, true):
    return len(set(true) & set(test)) / len(set(true) | set(test))

# def dtw(test, true):
#     # https://www.geeksforgeeks.org/dynamic-time-warping-dtw-in-time-series/
#     test_s = pd.Series(test).fillna(method="ffill").values
#     true_s = pd.Series(true).fillna(method="ffill").values
#     min_length = min(len(test_s), len(true_s))
#     test_s = test_s[:min_length]
#     true_s = true_s[:min_length]
#     return dtw.distance(test_s, true_s)



tilt_switch_changepoints_data = {}
with open('../segmentation/tilt switches/change_points_2.json') as json_file:
    tilt_switch_changepoints_data = json.load(json_file)

scores = {}
for dataset in files:
    print(dataset)
    df = pd.read_csv(os.path.join(folder_path, "{}.csv".format(dataset)))
    stability_changepoints = []
    prev = None
    # Generate breakpoints form stability classifier
    for idx, row in df.iterrows():
        if idx == 0:
            prev = row
            continue

        if row['stability'] != prev['stability']:
            stability_changepoints.append(idx)
            prev = row

    # Generate scores for each dataset, for each configuration
    scores[dataset] = {}
    configs = tilt_switch_changepoints_data[dataset].keys()
    for config in configs:
        scores[dataset][config] = {}
        ops = tilt_switch_changepoints_data[dataset][config]
        for op in ops:
            test_data = tilt_switch_changepoints_data[dataset][config][op]
            scores[dataset][config][op] = {
                'intersect': intersect(test_data, stability_changepoints),
                # 'mse': mse(test_data, stability_changepoints),
                'jaccard': jaccard(test_data, stability_changepoints),
                # 'dtw': dtw(test_data, stability_changepoints),
            }
            print(scores[dataset][config][op])

# Write out the best performing setup for each configuration
for dataset in files:
    best_intersect = {
        'score': -1,
        'setup': {}
    }
    best_jaccard = {
        'score': -1,
        'setup': {}
    }
    for config in tilt_switch_changepoints_data[dataset].keys():
        for op in tilt_switch_changepoints_data[dataset][config].keys():
            val = scores[dataset][config][op]
            if val['intersect'] > best_intersect['score']:
                best_intersect['score'] = val['intersect']
                best_intersect['setup'] = {
                    'config': config,
                    'op': op
                }
            if val['jaccard'] > best_jaccard['score']:
                best_intersect['score'] = val['jaccard']
                best_intersect['setup'] = {
                    'config': config,
                    'op': op
                }
    print(best_intersect, best_jaccard)
    scores[dataset]['best'] = {
        'intersect': best_intersect,
        'jaccard': best_intersect
    }

# Count number of times a specific configuration was best
possible_configurations = {
    'compare(change)': {'or': 0, 'xor': 0, 'and': 0, 'xnor': 0},
    'change(compare)': {'or': 0, 'xor': 0, 'and': 0, 'xnor': 0},
}
for dataset in files:
    best_setup = scores[dataset]['best']['jaccard']['setup']
    possible_configurations[best_setup['config']][best_setup['op']] += 1
scores['best_overall'] = possible_configurations

with open('scores.json', 'w') as out_file:
    out_file.write(json.dumps(scores, indent=4))