import os

import pandas as pd


def read_silver_weather():
    input_path = "data/silver/weather_clean.csv"

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Silver file not found: {input_path}")

    return pd.read_csv(input_path)


def create_weather_summary(df):
    summary_df = (
        df.groupby("city")
        .agg(
            avg_temperature=("temperature", "mean"),
            min_temperature=("temperature", "min"),
            max_temperature=("temperature", "max"),
            record_count=("temperature", "count"),
        )
        .reset_index()
    )

    return summary_df


def save_to_gold(df):
    output_dir = "data/gold"
    output_path = os.path.join(output_dir, "weather_summary.csv")

    os.makedirs(output_dir, exist_ok=True)

    df.to_csv(output_path, index=False)

    print(f"Weather summary saved to {output_path}")


if __name__ == "__main__":
    silver_df = read_silver_weather()
    gold_df = create_weather_summary(silver_df)
    save_to_gold(gold_df)
