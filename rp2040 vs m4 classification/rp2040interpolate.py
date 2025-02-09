import pandas as pd

rp2040df = pd.read_csv("28-01_rp2040.csv")

m4df = pd.read_csv("28-01_rp2040.csv")
m4df.set_index('timestamp', inplace=True) # set column 'date' to index

for idx, row in rp2040df.iterrows():
    tw = m4df.loc[row['timestamp']]['stability']
    rp2040df.loc[idx,'true_wear'] = tw if isinstance(tw, str) else tw[0]

rp2040df.to_csv("rp2040interpolated.csv")
pass