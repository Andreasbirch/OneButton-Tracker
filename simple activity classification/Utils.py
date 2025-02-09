import pandas as pd
import sklearn

def confusion_matrix_scores(data, test_column, true_column):
    _df = pd.DataFrame(data)
    labels = ['in motion', 'on table', 'stable']
    report = sklearn.metrics.classification_report(_df[test_column], _df[true_column], labels=labels, target_names=labels, output_dict=True)
    return {
        'accuracy': report['accuracy'] if 'accuracy' in report else None,
        'avg': report['macro avg'],
        'weighted': report['weighted avg'],
    }