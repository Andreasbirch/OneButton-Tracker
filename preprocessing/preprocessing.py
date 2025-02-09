## Load all datasets one by one
## For each data set, create a normalized record
## Dataset indicated as being split up (i.e. _1, _2 suffix) are joined
## Timestamp, acceleration(normal), tilt_x, tilt_y, activity_classification(if applicable), stability_classification(if applicable), vbat (if applicable)
import json
import os
import re
from io import StringIO
from operator import truth

import numpy as np
import pandas as pd
from pandas.core.computation.ops import isnumeric

classification_dict = {
    0: 'Unknown',
    1: 'On Table',
    2: 'Stationary',
    3: 'Stable',
    4: 'In motion'
}

# Iterate the files in ../alle dataset. Picks only files named MM-dd, and only csv files
folder_path = "../alle dataset/"
file_paths = []
for device in ["m4", "rp2040"]:
    for file_path in os.listdir(folder_path + device):
        if re.match("\d{2}-\d{2}\.csv", file_path):
            file_paths.append(os.path.join(folder_path, device, file_path))
print(file_paths)

out_path = "out/"
def parse_activity(json_string):
    json_str = json_string.replace("'", '"').replace(';', ',')
    parsed_dict = json.loads(f"{{{json_str}}}")
    return parsed_dict.get('most_likely')

def parse_stability(json_string):
    if isinstance(json_string, int):
        return classification_dict[json_string]
    return json_string

def process_file(file_path, write_out = False):
    file_path = next(fp for fp in file_paths if fp.endswith(file_path))


    with open(file_path, 'r') as infile:
        processed_data = infile.read().replace('{', '"').replace('}', '"')

    df = pd.read_csv(StringIO(processed_data), header=0, quotechar='"')
    df.rename(columns={'tilt_up': 'tilt_x', 'tilt_forward': 'tilt_y', 'activity_classification': 'activity', 'stability_classification': 'stability', 'Timestamp':'timestamp'}, inplace=True)


    if pd.api.types.is_numeric_dtype(df['timestamp']):
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    else:
        df['timestamp'] = pd.to_datetime(df['timestamp'])

    if 'acc_magnitude' not in df.columns:
        df['acc_magnitude'] = np.sqrt(df['acc_x'] ** 2 + df['acc_y'] ** 2 + df['acc_z'] ** 2)

    columns = ['timestamp', 'acc_magnitude', 'tilt_x', 'tilt_y']
    if 'acc_x' in df.columns:
        columns.append('acc_x')
        columns.append('acc_y')
        columns.append('acc_z')
    if 'activity' in df.columns:
        columns.append('activity')
        df['activity'] = df['activity'].apply(parse_activity)
    if 'stability' in df.columns:
        columns.append('stability')
        df['stability'] = df['stability'].apply(parse_stability)


    if not write_out:
        return df
    else:
        #Write out the following columns: ## Timestamp, acceleration(normal), tilt_x, tilt_y, activity_classification(if applicable), stability_classification(if applicable), vbat (if applicable)
        df.to_csv(os.path.join(out_path, os.path.basename(file_path)), columns=columns, index=False)
process_file("../alle dataset/m4/28-01.csv", True)
# process_file("04-11.csv", True)
# for file_path in file_paths:
#     print(file_path)
#     process_file(file_path, True)
