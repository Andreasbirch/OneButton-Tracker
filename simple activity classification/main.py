import json
import os
import pandas as pd
from AccelerometerClassifier import AccelerometerClassifier
from TiltSwitchClassifier import TiltSwitchClassifier
from MixedClassifier import MixedClassifier

# Tanken her er stadig at kigge på stability, men prøve at vurdere om vi kan sige noget om nonwear, stable og in motion


folder_path = "../data/data"
files = [
    # "02-12",
    # "04-11",
    # "07-10",
    # "08-10",
    # "09-10",
    # "10-10",
    # "25-11",
    # "29-10",
    # Tilt switch sets
    # "11-01",
    '18-01'
]

out = {}
threshold = 2.49
for file_path in files:
    df = pd.read_csv(os.path.join(folder_path, "{}.csv".format(file_path)))
    # acc_classifier = AccelerometerClassifier(df, file_path, threshold)
    # tilt_classifier = TiltSwitchClassifier(df, file_path,  still_duration=3208)
    mix_classifier = MixedClassifier(df, file_path, threshold)

    out[file_path] = {
        # 'accelerometer': acc_classifier.classify(),
        # 'tilt_switch': tilt_classifier.classify(),
        "mixed": mix_classifier.classify(),
    }

with open('out_18_01_better_durations_classification.json', 'w') as out_file:
    out_file.write(json.dumps(out, indent=4))