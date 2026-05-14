import pandas as pd


def validate_weather_data(df):
    required_columns = [
        "city",
        "temperature",
        "condition",
        "timestamp"
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    if df.empty:
        raise ValueError("DataFrame is empty")

    if df["temperature"].isnull().sum() > 0:
        raise ValueError("Temperature column contains null values")

    print("Data quality validation passed")


if __name__ == "__main__":
    df = pd.read_csv("data/bronze/weather.csv")
    validate_weather_data(df)
