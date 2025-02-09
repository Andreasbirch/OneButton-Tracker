import json
import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from claspy.segmentation import BinaryClaSPSegmentation
from claspy.data_loader import load_has_dataset

#https://github.com/ermshaua/claspy?tab=readme-ov-file

folder_path = "../../data/data"
change_points_path = "../../data/change points"
out_obj = {}

for file_path in os.listdir(folder_path):
    print(file_path)
    df = pd.read_csv(os.path.join(folder_path, file_path))

    change_points = [42, 109, 2705, 2754, 2879, 3714]

    df.index = df['timestamp']
    # Observable example only uses data from earlier than 11 o clock (9 utc), so we do the same


    clasp = BinaryClaSPSegmentation()

    ## Full length data
    true_cps = np.array(change_points)
    out_obj[file_path] = {'true':change_points, 'test': {'univariate': [], 'multivariate': []}}

    predict_uni = clasp.fit_predict(df['acc_magnitude'].to_numpy())

    # clasp.plot(gt_cps=np.array([102, 473, 952, 1025, 7197, 7285, 7433, 8017, 9963, 10951]), heading="{} univariate".format(file_path), ts_name="acc_magnitude", file_path="{} univariate.png".format(file_path))
    clasp.plot(gt_cps=true_cps,
               heading="{} univariate".format(file_path), ts_name="acc_magnitude",
               file_path="{} univariate.png".format(file_path))
    out_obj[file_path]['test']['univariate'] = predict_uni
    print(predict_uni)

    if 'acc_x' in df.columns:
        predict_multi = clasp.fit_predict(df[['acc_x','acc_y','acc_z']].to_numpy())
        clasp.plot(gt_cps=true_cps,
                   heading="{} multivariate".format(file_path),
                   ts_name="acc",
                   file_path="{} multivariate.png".format(file_path))
        out_obj[file_path]['test']['multivariate'] = predict_uni
        print(predict_multi)

    ## Data before 9 (11 UTC)
    # df = df.between_time("0:00", "11:00")
    # clasp.fit_predict(df['acc_magnitude'].to_numpy())
    # clasp.plot(gt_cps=true_cps, heading="Accelerometer readings during various activities", ts_name="acc_magnitude", file_path="08-10 before 9.png")
    #
    # clasp.fit_predict(df[['acc_x','acc_y','acc_z']].to_numpy())
    # clasp.plot(gt_cps=true_cps, heading="Accelerometer readings during various activities", ts_name="acc", file_path="08-10 before 9 multivariate.png")
    pass
