import os
from datetime import datetime

import pandas as pd
import requests


def fetch_weather_data():
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": 59.91,
        "longitude": 10.75,
        "current_weather": True
    }

    response = requests.get(url, params=params)

    data = response.json()

    current_weather = data["current_weather"]

    weather_data = {
        "city": ["Oslo"],
        "temperature": [current_weather["temperature"]],
        "windspeed": [current_weather["windspeed"]],
        "timestamp": [datetime.now()]
    }

    return pd.DataFrame(weather_data)


def save_to_bronze(df):
    output_dir = "data/bronze"
    output_path = os.path.join(output_dir, "real_weather.parquet")

    os.makedirs(output_dir, exist_ok=True)

    df.to_parquet(output_path, index=False)

    print(f"Real weather data saved to {output_path}")


if __name__ == "__main__":
    weather_df = fetch_weather_data()
    print(weather_df)

    save_to_bronze(weather_df)
