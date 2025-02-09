import pandas as pd
import Utils

class TiltSwitchClassifier:
    def __init__(self, _df, name, still_duration):
        self.df = _df.copy(deep=True)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.name = name
        self.still_duration = still_duration

    def true_wear(self, row):
        return row['stability'].lower()

    def test_wear(self, chunk, still_duration, moving_duration):
        first = chunk[0]['timestamp']
        last = chunk[-1]['timestamp']
        seconds_diff = (last - first).total_seconds()

        if seconds_diff > still_duration:
            return 'on table'
        if seconds_diff < moving_duration:
            return 'in motion'
        else:
            return 'stable'

    def generate_time_chunks(self, df):
        first_row = df.iloc[0]
        prev_x = first_row['tilt_x']
        prev_y = first_row['tilt_y']
        chunk = [first_row]

        time_chunks = []
        breakpoints = []

        for idx, row in df.iterrows():
            if idx == 0: continue
            current_x = row['tilt_x']
            current_y = row['tilt_y']

            change_x = current_x != prev_x
            change_y = current_y != prev_y

            if change_x or change_y:
                time_chunks.append(chunk)
                breakpoints.append({'index': idx, 'timestamp':row['timestamp']})
                prev_x = current_x
                prev_y = current_y
                chunk = []

            chunk.append(row)
        time_chunks.append(chunk)
        return time_chunks, breakpoints

    def classify(self):
        print("classifying {} duration {}".format(self.name, self.still_duration))
        time_chunks, breakpoints = self.generate_time_chunks(self.df)
        out = {}
        for duration in range(100):
            data = []
            for chunk in time_chunks:
                for row in chunk:
                    data.append({
                        'timestamp': row['timestamp'],
                        'acceleration': row['acc_magnitude'],
                        'test_wear': self.test_wear(chunk, self.still_duration, duration),
                        'true_wear': self.true_wear(row),
                        'dataset': self.name,
                        'type': 'tilt_switch'
                    })
            out[duration] = Utils.confusion_matrix_scores(data, 'test_wear', 'true_wear')
        return out