import pandas as pd
import sklearn

def confusion_matrix_scores(data, test_column, true_column):
    _df = pd.DataFrame(data)

    tn, fp, fn, tp = sklearn.metrics.confusion_matrix(_df[true_column], _df[test_column]).ravel()
    tn = int(tn)
    fp = int(fp)
    fn = int(fn)
    tp = int(tp)

    out = {
        'confusion_matrix': {
            'tn': tn,
            'fp': fp,
            'fn': fn,
            'tp': tp
        },
        'metrics': {
            'accuracy': (tp + tn) / (tp + tn + fp + fn),
            'precision': tp / (tp + fp),
            'recall': tp / (tp + fn),
            'f1': 2 * tp / (2 * tp + fp + fn),
        }
    }

    out['metrics']['avg'] = (out['metrics']['accuracy'] + out['metrics']['precision'] + out['metrics']['recall'] + out['metrics']['f1']) / 4
    return out