import pandas as pd
import statistics
import Utils
import sklearn
from sklearn import metrics
from sklearn.metrics import confusion_matrix

class AccelerometerClassifier:
    def __init__(self, _df, name, moving_threshold, window_size = 11, std_dev_threshold = 0.05):
        self.df = _df.copy(deep=True)
        self.name = name
        self.moving_threshold = moving_threshold

        # Vi laver klassifieren med hvad vi kom frem til var et optimalt vindue på 11
        # Og et stdDev threshold på 0.05
        self.window_size = window_size
        self.std_dev_threshold = std_dev_threshold

    def true_wear(self, row):
        return row['stability'].lower()

    def test_wear(self, window):
        params = ['acc_x', 'acc_y', 'acc_z'] if 'acc_x' in self.df.columns else ['acc_magnitude']

        for param in params:
            standard_dev = statistics.stdev(window[param])
            if standard_dev <= self.std_dev_threshold:
                return 'on table'
            if self.std_dev_threshold < standard_dev < self.moving_threshold:
                return 'stable'
            else:
                return 'in motion'



    def classify(self):
        df = self.df
        print("classifying {}".format(self.name))



        data = []

        for idx, row in df.iterrows():
            # Math.max(0, i - Math.floor(sampleWindow / 2)),
            # Math.min(bno_data_11_6.length, i + Math.floor(sampleWindow / 2))
            window = df.iloc[max(0, idx - self.window_size // 2):min(idx + self.window_size // 2, len(df))]

            data.append({
                'timestamp': row['timestamp'],
                'acceleration': row['acc_magnitude'],
                'test_wear': self.test_wear(window),
                'true_wear': self.true_wear(row),
                'dataset': self.name,
                'type': 'accelerometer'
            })

        return Utils.confusion_matrix_scores(data, 'test_wear', 'true_wear')



