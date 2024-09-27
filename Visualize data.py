#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Visualize Data gathered between 21. and 23. september

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from collections import Counter
from enum import Enum

class sample_types(Enum):
    most_occuring = 1
    hierarchical = 2 #Running > Walking > In-Vehicle > Still > Unknown

df = pd.read_csv('data 21-23 sep/data 123.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Group into approximately 15 minute sections, aligning with hourly quarters
df = df.set_index('timestamp')
df['group'] = df.index.to_series().groupby(pd.Grouper(freq='15min')).ngroup() + 1
df = df.reset_index() 

out_list = []

first_timestamp = df['timestamp'][0]
new_timestamp = datetime(first_timestamp.year, first_timestamp.month, first_timestamp.day, first_timestamp.hour, first_timestamp.minute, 0)
occ= None
sample_type = sample_types.hierarchical
## Select most prevalent activity for each minute
for _,group in df.groupby(df['group']):
    # most_frequent_activity = Counter(group['activity_classification']).most_common(1)[0][0]
    occurrences = group['activity_classification'].value_counts()
    activity = None
    if sample_type == sample_types.most_occuring:
        activity = occurrences.index[0]
    elif sample_type == sample_types.hierarchical:#Running > Walking > In-Vehicle > Still > Unknown
        for i in ['Running', 'Walking', 'In-Vehicle', 'Still', 'Unknown']:
            if i in occurrences.index:
                activity = i
                break
    new_timestamp = group['timestamp'].iloc[0]
    out_list.append((new_timestamp, activity))
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