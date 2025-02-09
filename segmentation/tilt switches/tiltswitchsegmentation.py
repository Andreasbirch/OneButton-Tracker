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

change_points = {}

for dataset in files:
    print(dataset)
    df = pd.read_csv(os.path.join(folder_path, "{}.csv".format(dataset)))
    first_row = df.iloc[0]
    _change_points = {
        'a': {
            'tilt_x': [],
            'tilt_y': [],
            'or': [],
            'xor': [],
            'and': [],
            'xnor': []
        },
        'b': {
            'tilt_x': [],
            'tilt_y': [],
            'or': [],
            'xor': [],
            'and': [],
            'xnor': []
        },
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
        _or = row['tilt_x'] | row['tilt_y']
        _xor = row['tilt_x'] ^ row['tilt_y']
        _and = row['tilt_x'] & row['tilt_y']
        _xnor = row['tilt_x'] == row['tilt_y']

        for (op, val) in [('tilt_x', row['tilt_x']), ('tilt_y', row['tilt_y']), ('or', _or), ('xor', _xor ), ('and', _and), ('xnor', _xnor)]:
            if (prev[op] is None) or (val != prev[op]):
                _change_points['a'][op].append(idx)
                prev[op] = val

    for idx, row in df.iterrows():
        change_x = row['tilt_x'] != prev['tilt_x']
        change_y = row['tilt_y'] != prev['tilt_y']

        _or = change_x | change_y
        _xor = change_x ^ change_y
        _and = change_x & change_y
        _xnor = change_x == change_y

        for (op, val) in [('tilt_x', row['tilt_x']), ('tilt_y', row['tilt_y']), ('or', _or), ('xor', _xor ), ('and', _and), ('xnor', _xnor)]:
            if (prev[op] is None) or (val != prev[op]):
                _change_points['b'][op].append(idx)
                prev[op] = val

        prev['tilt_x'] = row['tilt_x']
        prev['tilt_y'] = row['tilt_y']
    print(_change_points)
    change_points[dataset] = _change_points

print(change_points)
with open('change_points.json', 'w') as out_file:
    out_file.write(json.dumps(change_points, indent=4))


def change(curr, prev):
    return None

def compare(a, b):
    return None
a = True
b = True
# 1
change(compare(a,b), compare(a,b))
compare(change(a,b), change(a,b))