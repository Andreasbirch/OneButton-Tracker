import pandas as pd
from datetime import datetime

## Provide path to csv
path_to_csv = "/Users/andreasbirch/Desktop/obt tests 08-10/data 1.csv"

## Provide either the first or the last time of the time series. The time series will be based off of this
## Format YYYY-MM-dd hh:mm:ss
start_time = "2024-10-09 09:37:29"
end_time = "2024-10-08 11:59:07"

## Flag if csv file should be overwritten
overwrite = False

df = pd.read_csv(path_to_csv, delimiter=',', header=None)
df[0] = pd.to_datetime(df[0])

corrected_times = []

if start_time != None:
    start_datetime = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    time_delta = start_datetime - df[0].iloc[0]
    df[0] = df[0] + time_delta

if end_time != None:
    end_datetime = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    time_delta = end_datetime - df[0].iloc[-1]
    df[0] = df[0] + time_delta
    
if not overwrite:
    df.to_csv(path_to_csv, index=False, header=False, sep=';')
    