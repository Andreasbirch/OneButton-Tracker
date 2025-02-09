import json
import os
import pandas as pd
from AccelerometerClassifier import AccelerometerClassifier
from TiltSwitchClassifier import TiltSwitchClassifier
from MixedClassifier import MixedClassifier

folder_path = "../data/data"
files = [
    "02-12",
    "04-11",
    "07-10",
    "08-10",
    "09-10",
    "10-10",
    "25-11",
    "29-10",
    # Deep sleep sets
    "11-01",
    '18-01'
]

out = {}
for file_path in files:
    df = pd.read_csv(os.path.join(folder_path, "{}.csv".format(file_path)))
    if 'activity' not in df.columns: continue

    acc_classifier = AccelerometerClassifier(df, file_path, 'activity')
    tilt_classifier = TiltSwitchClassifier(df, file_path, 'activity', [3208])
    mix_classifier = MixedClassifier(df, file_path, 'activity')
    out[file_path] = {
        'accelerometer': acc_classifier.classify(),
        'tilt_switch': tilt_classifier.classify(),
        "mixed": mix_classifier.classify(),
    }

with open('out_alle_dataset_true_er_activity.json', 'w') as out_file:
    out_file.write(json.dumps(out, indent=4))