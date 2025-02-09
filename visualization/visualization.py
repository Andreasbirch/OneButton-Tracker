import os
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px





file_path = "../data/data/10-10.csv"
df = pd.read_csv(file_path)

# df = df.reset_index()
fig = px.line(df, x='timestamp', y='acc_magnitude', hover_data={'index': df.index}, title=file_path)
fig.update_layout(
    xaxis=dict(
        rangeslider=dict(visible=True),
        title='Timestamp'
    ),
    yaxis=dict(
        title='Acc Magnitude'
    ),
    hovermode='x unified'
)
fig.show()



# for file_path in os.listdir(folder_path):
#     df = pd.read_csv(os.path.join(folder_path, file_path))
#     plt.plot(df['acc_magnitude'])
#     plt.title(file_path)
#     plt.show()
#     continue