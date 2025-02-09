## Test that there are no jumps back in time in the datasets.
#If there is, print out the gaps
import os
import pandas as pd

folder_path = "../data/data"
out_obj = {}

for file_path in os.listdir(folder_path):
    print(file_path)
    df = pd.read_csv(os.path.join(folder_path, file_path))
    time_jumps = []
    curr_time = df.iloc[0]['timestamp']
    for i, row in enumerate(df['timestamp']):
        if row < curr_time:
            time_jumps.append([i, curr_time, row])
        curr_time = row

    if len(time_jumps) > 0:
        print("Idx", "curr", "next")
        for time_jump in time_jumps:
            print(time_jump)

