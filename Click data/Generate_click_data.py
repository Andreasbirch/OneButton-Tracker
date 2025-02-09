import pandas as pd
import numpy as np

# Load the original dataset
original_file = "../Datasets/click_data.csv"  # Replace with your file path
data = pd.read_csv(original_file)

# Rename columns for clarity (adjust based on your dataset structure)
data.columns = ['Timestamp', 'Value1', 'Value2']

# Convert the timestamp column to datetime
data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%Y%m%dT%H%M%SZ')

# Generate the time range for approximately one year
start_date = data['Timestamp'].min()
end_date = start_date + pd.Timedelta(days=365)

# Calculate intervals based on the original dataset
time_deltas = data['Timestamp'].diff().dropna().dt.total_seconds()

# Generate random intervals similar to the original dataset's distribution
np.random.seed(42)  # For reproducibility
intervals = np.random.choice(time_deltas, size=365 * 24, replace=True)
new_timestamps = pd.to_datetime(np.cumsum(intervals), unit='s', origin=start_date)
new_timestamps = new_timestamps[new_timestamps <= end_date]  # Restrict to one year

# Generate synthetic values for Value1 and Value2
value1_new = np.random.choice(data['Value1'], size=len(new_timestamps), replace=True)
value2_new = np.random.choice(data['Value2'], size=len(new_timestamps), replace=True)

# Create the new dataset
new_data = pd.DataFrame({
    'Timestamp': new_timestamps,
    'Value1': value1_new,
    'Value2': value2_new
})

# Save the new dataset to a CSV file
output_file = "generated_data.csv"  # Replace with your desired output path
new_data.to_csv(output_file, index=False)

print(f"New dataset saved to: {output_file}")
