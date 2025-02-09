import json

with open('out_alle_dataset_true_er_stability.json', 'r') as file:
    data = json.loads(file.read())

    out = {
        'accelerometer': None,
        'tilt_switch': None,
        'mixed': None
    }

    for dataset in data:
        for classifier in data[dataset]:
            scores = data[dataset][classifier]['3208' if classifier == 'tilt_switch' else 'confusion_matrix']
            if not out[classifier]:
                out[classifier] = scores
            else:
                for score in scores:
                    out[classifier][score] += scores[score]
    for classifier in out:
        for score in out[classifier]:
            out[classifier][score] /= len(data)

with open('out_alle_dataset_true_er_stability_averages.json', 'w') as out_file:
    out_file.write(json.dumps(out, indent=4))