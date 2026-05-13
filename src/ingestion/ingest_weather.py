import pandas as pd
from datetime import datetime

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

    df = pd.DataFrame(data)

    print("Weather data fetched successfully")
    print(df)

    return df


if __name__ == "__main__":
    fetch_weather_data()
