import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Simulation Parameters
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 7, 1)
ACTIVE_HOURS_WEEKDAY = (7, 23)  # Active from 7 AM to 11 PM
ACTIVE_HOURS_WEEKEND = (10, 1)  # Active from 10 AM to 1 AM
FORGOTTEN_DAYS = 2  # Days per month the device is forgotten
BUTTON_PRESS_PROB_PER_MINUTE = 0.02  # Probability of button press per minute
BUTTON_PRESS_DURATION_MEAN = 400  # Average button press duration in ms
BUTTON_PRESS_DURATION_STD = 100  # Standard deviation for press duration
SAMPLE_INTERVAL = 60  # Sampling every 60 seconds to reduce dataset size
SPECIAL_BUTTON_PRESS_DATE = datetime(2024, 3, 15)  # Abnormal button press day

# Initialize data storage
data = []
current_date = START_DATE

# Generate data day by day
while current_date < END_DATE:
    is_weekend = current_date.weekday() >= 5
    active_start, active_end = (ACTIVE_HOURS_WEEKEND if is_weekend else ACTIVE_HOURS_WEEKDAY)

    # Handle forgotten device days
    if random.random() < (FORGOTTEN_DAYS / 30):
        current_date += timedelta(days=1)
        continue

    start_time = current_date.replace(hour=active_start % 24, minute=0, second=0)
    end_time = (current_date + timedelta(days=1)).replace(hour=active_end % 24, minute=0, second=0)

    while start_time < end_time:
        acc_x = random.uniform(-1, 1)
        acc_y = random.uniform(-1, 1)
        acc_z = random.uniform(9.5, 10.5)
        acc_magnitude = (acc_x ** 2 + acc_y ** 2 + acc_z ** 2) ** 0.5
        tilt_x = random.choice([0, 1])
        tilt_y = random.choice([0, 1])

        # Button press logic
        if current_date == SPECIAL_BUTTON_PRESS_DATE or random.random() < BUTTON_PRESS_PROB_PER_MINUTE:
            reason = 1
            duration = max(100, int(random.gauss(BUTTON_PRESS_DURATION_MEAN, BUTTON_PRESS_DURATION_STD)))
        else:
            reason = 0
            duration = 0

        data.append([
            start_time,
            acc_magnitude,
            reason,
            duration,
            tilt_x,
            tilt_y
        ])

        start_time += timedelta(seconds=SAMPLE_INTERVAL)

    current_date += timedelta(days=1)

# Create DataFrame
df = pd.DataFrame(data, columns=['timestamp', 'acc_magnitude', 'reason', 'duration', 'tilt_x', 'tilt_y'])

# Save to CSV
output_file = 'simulated_device_data.csv'
df.to_csv(output_file, index=False)
print(f"Data saved to {output_file}")
