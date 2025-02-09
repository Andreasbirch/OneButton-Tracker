import json
import os
from itertools import compress

import pandas as pd

folder_path = "../../data/data"
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

def change(curr, prev):
    return curr != prev

def compare(a, b):
    _or = a | b
    _xor = a ^ b
    _and = a & b
    _xnor = a == b
    return {
        'or': _or,
        'xor': _xor,
        'and': _and,
        'xnor': _xnor
    }

def compare_change(df):
    change_points_change = {
        'or': [],
        'xor': [],
        'and': [],
        'xnor': []
    }
    prev = {
        'tilt_x': None,
        'tilt_y': None,
        'or': None,
        'xor': None,
        'and': None,
        'xnor': None
    }

    for idx, row in df.iterrows():
        if idx == 0:
            prev['tilt_x'] = row['tilt_x']
            prev['tilt_y'] = row['tilt_y']
            continue

        change_x = change(row['tilt_x'], prev['tilt_x'])
        change_y = change(row['tilt_y'], prev['tilt_y'])

        compare_curr = {
            'or': change_x | change_y,
            'xor': change_x ^ change_y,
            'and': change_x & change_y,
            'xnor': change_x == change_y
        }

        for op, val in compare_curr.items():
            if (prev[op] is None) or (val != prev[op]):
                change_points_change[op].append(idx)
                prev[op] = val
        prev['tilt_x'] = row['tilt_x']
        prev['tilt_y'] = row['tilt_y']
    return change_points_change

def change_compare(df): # change(compare, compare)
    change_points_change = {
        'or': [],
        'xor': [],
        'and': [],
        'xnor': []
    }
    prev = {
        'tilt_x': None,
        'tilt_y': None,
        'or': None,
        'xor': None,
        'and': None,
        'xnor': None
    }

    for idx, row in df.iterrows():
        if idx == 0:
            prev['tilt_x'] = row['tilt_x']
            prev['tilt_y'] = row['tilt_y']
            continue

        curr_x = row['tilt_x']
        curr_y = row['tilt_y']
        prev_x = prev['tilt_x']
        prev_y = prev['tilt_y']

        compare_curr = {
            'or': change((curr_x | prev_x), (curr_y | prev_y)),
            'xor': change((curr_x ^ prev_x), (curr_y ^ prev_y)),
            'and': change((curr_x & prev_x), (curr_y & prev_y)),
            'xnor': change((curr_x == prev_x), (curr_y == prev_y)),
        }

        for op, val in compare_curr.items():
            if (prev[op] is None) or (val != prev[op]):
                change_points_change[op].append(idx)
                prev[op] = val
        prev['tilt_x'] = curr_x
        prev['tilt_y'] = curr_y
    return change_points_change

change_points = {}
for dataset in files:
    print(dataset)
    df = pd.read_csv(os.path.join(folder_path, "{}.csv".format(dataset)))
    change_points[dataset] = {
        'compare(change)': compare_change(df),
        'change(compare)': change_compare(df)
    }

print(change_points)
with open('change_points_2.json', 'w') as out_file:
    out_file.write(json.dumps(change_points, indent=4))