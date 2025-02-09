import statistics
from datetime import datetime

import Utils
import pandas as pd
from itertools import chain

class MixedClassifier:
    def __init__(self, _df, name, moving_threshold, std_dev_threshold=0.05):
        self.df = _df.copy(deep=True)
        self.name = name
        self.moving_threshold = moving_threshold

        # Og et stdDev threshold på 0.05
        self.std_dev_threshold = std_dev_threshold

    def true_wear(self, row):
        return row['stability'].lower()

    def test_wear(self, window):
        _df = pd.DataFrame(window)
        first = datetime.strptime(_df.iloc[0]['timestamp'], '%Y-%m-%d %H:%M:%S')
        last = datetime.strptime(_df.iloc[-1]['timestamp'], '%Y-%m-%d %H:%M:%S')
        seconds_diff = (last - first).total_seconds()
        if seconds_diff >= 3208:
            return 'on table'

        params = ['acc_x', 'acc_y', 'acc_z'] if 'acc_x' in self.df.columns else ['acc_magnitude']

        for param in params:
            standard_dev = statistics.stdev(_df[param])
            if standard_dev <= self.std_dev_threshold:
                return 'on table'
            if self.std_dev_threshold < standard_dev < self.moving_threshold:
                return 'stable'
            else:
                return 'in motion'

    def merge_single_element_lists(self, lists):
        if not lists:
            return []

        merged_lists = []
        i = 0

        while i < len(lists):
            if len(lists[i]) == 1:
                if i == 0:
                    lists[i + 1] = lists[i] + lists[i + 1]
                elif i == len(lists) - 1:
                    merged_lists[-1] += lists[i]
                else:
                    lists[i + 1] = lists[i] + lists[i + 1]
                i += 1
            else:
                merged_lists.append(lists[i])
            i += 1

        return merged_lists

    def generate_time_chunks(self, df):
        first_row = df.iloc[0]
        prev_x = first_row['tilt_x']
        prev_y = first_row['tilt_y']
        chunk = [first_row]
        #df[df['timestamp'] < '2024-10-08 11:00:00']
        #df[pd.DataFrame(chain.from_iterable(time_chunks))['timestamp'] < '2024-10-08 11:00:00']
        time_chunks = []
        breakpoints = []

        for idx, row in df.iterrows():
            if idx == 0: continue
            current_x = row['tilt_x']
            current_y = row['tilt_y']

            change_x = current_x != prev_x
            change_y = current_y != prev_y

            if change_x or change_y:
                if len(chunk) > 1:
                    time_chunks.append(chunk)
                else:
                    time_chunks[-1].append(chunk[0])
                breakpoints.append({'index': idx, 'timestamp': row['timestamp']})
                prev_x = current_x
                prev_y = current_y
                chunk = []

            chunk.append(row)
        if len(chunk) > 1:
            time_chunks.append(chunk)
        else:
            time_chunks[-1].append(chunk[0])

        print(len(list(chain.from_iterable(time_chunks))))
        return time_chunks, breakpoints

    def classify(self):
        print(f"classifying {self.name}")
        time_chunks, breakpoints = self.generate_time_chunks(self.df)
        data = []
        for chunk in time_chunks:
            test_wear_result = self.test_wear(chunk)
            for row in chunk:
                data.append({
                    'timestamp': row['timestamp'],
                    'acceleration': row['acc_magnitude'],
                    'test_wear': test_wear_result,
                    'true_wear': self.true_wear(row),
                    'dataset': self.name,
                    'type': 'tilt_switch'
                })

        return data #Utils.confusion_matrix_scores(data, 'test_wear', 'true_wear')