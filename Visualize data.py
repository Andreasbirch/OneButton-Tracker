#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Visualize Data gathered between 21. and 23. september

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from collections import Counter

df = pd.read_csv('data 21-23 sep/data 123.csv')
first_timestamp = datetime.strptime(df['timestamp'][0], '%Y-%m-%d %H:%M:%S')
# last_record = df[len(df)-1]

## Split into ~15 minute groups meaning 60*15 measurements
minute_groups = np.array_split(df, int(len(df)/900))


out_list = []

new_timestamp = datetime(first_timestamp.year, first_timestamp.month, first_timestamp.day, first_timestamp.hour, first_timestamp.minute, 0)

## Select most prevalent activity for each minute
for group in minute_groups:
    most_frequent_activity = Counter(group['activity_classification']).most_common(1)[0][0]
    a = group['timestamp']
    new_timestamp = group['timestamp'][0]
    out_list.append((new_timestamp, most_frequent_activity))
    # new_timestamp = new_timestamp + timedelta(minutes=15)



## Plot the data
colors = {'Unknown': 'gray',
          'Still': 'orange',
          'Walking': 'green',
          'In-Vehicle': 'blue',
          'Running': 'red'}

fig, ax = plt.subplots(figsize=(len(out_list), 2))
timestamps, values = zip(*out_list)

# Plot each timestamp as a small horizontal section
for i in range(len(timestamps) - 1):
    start = timestamps[i]
    end = timestamps[i+1]
    ax.barh(0, end - start, left=start, color=colors[values[i]], edgecolor='black')


# Set labels and limits
ax.set_yticks([])
ax.set_xticklabels(timestamps)
ax.set_xlim(timestamps[0], timestamps[len(timestamps)-1])

# Display the plot
plt.show()