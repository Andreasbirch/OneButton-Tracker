import statistics
import Utils
import pandas as pd

class MixedClassifier:
    def __init__(self, _df, name, true_classifier, std_dev_threshold=0.05):
        self.df = _df.copy(deep=True)
        self.name = name
        self.true_classifier = true_classifier

        # Og et stdDev threshold på 0.05
        self.std_dev_threshold = std_dev_threshold

    def true_wear(self, row):
        if self.true_classifier == 'stability':
            return row['stability'].lower() != 'on table'
        elif self.true_classifier == 'activity':
            return row['activity'].lower() != 'still'

    def test_wear(self, window):
        _df = pd.DataFrame(window)
        params = ['acc_x', 'acc_y', 'acc_z']

        if 'acc_x' in self.df.columns:
            for param in params:
                if statistics.stdev(_df[param]) >= self.std_dev_threshold:
                    return True
        else:
            if statistics.stdev(_df['acc_magnitude']) >= self.std_dev_threshold:
                return True
        return False

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
                breakpoints.append({'index': idx, 'timestamp': row['timestamp']})
                prev_x = current_x
                prev_y = current_y
                chunk = []

            chunk.append(row)
        time_chunks.append(chunk)

        time_chunks = self.merge_single_element_lists(time_chunks)

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

        return {
            # 'data': data,
            'confusion_matrix': Utils.confusion_matrix_scores(data, 'test_wear', 'true_wear')['metrics']
        }