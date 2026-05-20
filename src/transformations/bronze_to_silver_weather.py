import os

import pandas as pd


def read_bronze_weather():
    input_path = "data/bronze/real_weather.parquet"

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Bronze file not found: {input_path}")

    return pd.read_parquet(input_path)


def transform_weather_data(df):
    df = df.copy()

    df.columns = [column.strip().lower() for column in df.columns]

    df = df.dropna()

    df["city"] = df["city"].str.strip().str.lower()

    df["windspeed"] = df["windspeed"].astype(float)

    df["temperature"] = df["temperature"].astype(float)

    return df


def save_to_silver(df):
    output_dir = "data/silver"
    output_path = os.path.join(output_dir, "weather_clean.parquet")

    os.makedirs(output_dir, exist_ok=True)

    df.to_parquet(output_path, index=False)

    print(f"Clean weather data saved to {output_path}")


if __name__ == "__main__":
    bronze_df = read_bronze_weather()
    silver_df = transform_weather_data(bronze_df)
    save_to_silver(silver_df)
