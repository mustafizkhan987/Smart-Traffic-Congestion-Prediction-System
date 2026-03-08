import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Parameters
NUM_DAYS = 30
ROADS = ['ORR_23', 'MG_ROAD', 'HSR_LAYOUT_1', 'KORAMANGALA_100FT', 'WHITEFIELD_MAIN', 'ELECTRONIC_CITY_PHASE_1']
WEATHER_CONDITIONS = ['Clear', 'Rainy', 'Cloudy']
START_DATE = datetime.now() - timedelta(days=NUM_DAYS)

# Helper function to assign labels
def assign_congestion_label(vehicles, road_capacity):
    ratio = vehicles / road_capacity
    if ratio < 0.4:
        return 'Low'
    elif ratio < 0.75:
        return 'Medium'
    else:
        return 'High'

def generate_synthetic_data():
    print("Generating synthetic traffic data...")
    records = []
    
    # Capacity mappings for realistic variation
    road_capacities = {
        'ORR_23': 200,
        'MG_ROAD': 150,
        'HSR_LAYOUT_1': 100,
        'KORAMANGALA_100FT': 120,
        'WHITEFIELD_MAIN': 180,
        'ELECTRONIC_CITY_PHASE_1': 200
    }
    
    # Iterate through days
    for day_offset in range(NUM_DAYS):
        current_date = START_DATE + timedelta(days=day_offset)
        day_of_week = current_date.strftime('%A')
        
        # Determine if it's a weekend
        is_weekend = current_date.weekday() >= 5
        
        # Iterate through 24 hours (15-min intervals)
        for hour in range(24):
            for minute in [0, 15, 30, 45]:
                time_str = f"{hour:02d}:{minute:02d}"
                
                # Iterate through all roads to have data for each at this timestamp
                for road in ROADS:
                    capacity = road_capacities[road]
                    
                    # Base vehicle count
                    base_vehicles = capacity * 0.3 # 30% baseline
                    
                    # Time of day factors (Peak hours)
                    # Morning Peak: 8:00 - 10:30
                    if 8 <= hour < 11 and not is_weekend:
                        base_vehicles *= 2.5
                    # Evening Peak: 17:00 (5PM) - 20:00 (8PM)
                    elif 17 <= hour < 20 and not is_weekend:
                        base_vehicles *= 2.8
                    # Afternoon (slight bump)
                    elif 12 <= hour < 15:
                        base_vehicles *= 1.5
                    # Night (low traffic)
                    elif 0 <= hour < 5:
                        base_vehicles *= 0.2
                    
                    # Weekend logic (peaks are shifted or lower)
                    if is_weekend:
                        if 11 <= hour <= 21:
                            base_vehicles *= 1.4 # Constant moderate traffic on weekends
                    
                    # Weather factor
                    weather = random.choices(WEATHER_CONDITIONS, weights=[0.7, 0.2, 0.1])[0]
                    if weather == 'Rainy':
                        base_vehicles *= 1.3 # Rain slows down traffic, effectively increasing congestion
                        
                    # Add random noise
                    noise = np.random.normal(0, capacity * 0.1)
                    final_vehicles = max(0, int(base_vehicles + noise))
                    
                    # Sometimes anomalous traffic
                    if random.random() < 0.02: # 2% chance of sudden jam
                        final_vehicles = int(capacity * random.uniform(0.8, 1.2))
                    
                    # Assign label
                    congestion_label = assign_congestion_label(final_vehicles, capacity)
                    
                    records.append({
                        'Date': current_date.strftime('%Y-%m-%d'),
                        'Time': time_str,
                        'Day': day_of_week,
                        'Road_ID': road,
                        'Weather': weather,
                        'Vehicle_Count': final_vehicles,
                        'Congestion_Level': congestion_label
                    })

    df = pd.DataFrame(records)
    
    # Save to data directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'synthetic_traffic_data.csv')
    
    df.to_csv(output_path, index=False)
    print(f"Data generated successfully and saved to: {output_path}")
    print(f"Total records: {len(df)}")
    print("\nValue counts for Congestion_Level:")
    print(df['Congestion_Level'].value_counts())
    
    return df

if __name__ == "__main__":
    generate_synthetic_data()
