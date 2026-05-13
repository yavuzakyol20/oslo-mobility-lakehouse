import os
from datetime import datetime

import pandas as pd


def fetch_weather_data():
    data = {
        "city": ["Oslo", "Oslo", "Oslo"],
        "temperature": [12, 14, 11],
        "condition": ["Rain", "Cloudy", "Sunny"],
        "timestamp": [
            datetime.now(),
            datetime.now(),
            datetime.now()
        ]
    }

    return pd.DataFrame(data)


def save_to_bronze(df):
    output_dir = "data/bronze"
    output_path = os.path.join(output_dir, "weather.csv")

    os.makedirs(output_dir, exist_ok=True)

    df.to_csv(output_path, index=False)

    print(f"Weather data saved to {output_path}")


if __name__ == "__main__":
    weather_df = fetch_weather_data()
    save_to_bronze(weather_df)
