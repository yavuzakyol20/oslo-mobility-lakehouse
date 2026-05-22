import pandas as pd

from src.transformations.bronze_to_silver_weather import transform_weather_data


def test_transform_weather_data():
    sample_data = {
        "city": [" Oslo "],
        "temperature": [15],
        "windspeed": [5],
        "timestamp": ["2026-01-01"]
    }

    df = pd.DataFrame(sample_data)

    transformed_df = transform_weather_data(df)

    assert transformed_df["city"][0] == "oslo"
    assert transformed_df["temperature"][0] == 15.0
    assert transformed_df["windspeed"][0] == 5.0
