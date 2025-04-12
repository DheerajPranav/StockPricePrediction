import os
import pandas as pd
import ta  # Make sure to install with: pip install ta


def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values("date")
    df["date"] = pd.to_datetime(df["date"])

    # Price-based features
    df["return"] = df["close"].pct_change()
    df["ma5"] = df["close"].rolling(window=5).mean()
    df["ma10"] = df["close"].rolling(window=10).mean()
    df["ma20"] = df["close"].rolling(window=20).mean()

    # Volume/Volatility features
    df["vol_chg"] = df["volume"].pct_change()
    df["volatility"] = df["high"] - df["low"]

    # Technical indicators
    df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
    df["macd"] = ta.trend.MACD(df["close"]).macd()
    df["momentum"] = ta.momentum.ROCIndicator(df["close"]).roc()

    # Time-based features
    df["dayofweek"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["is_month_start"] = df["date"].dt.is_month_start.astype(int)
    df["is_month_end"] = df["date"].dt.is_month_end.astype(int)

    # Target: next day close
    df["target"] = df["close"].shift(-1)

    df = df.dropna()
    return df


def prepare_dataset():
    print("📦 Starting dataset preparation...")
    combined = []

    COLS_REQUIRED = ["date", "open", "high", "low", "close", "volume", "ticker"]

    for file in os.listdir("data"):
        if file.endswith(".csv"):
            try:
                df = pd.read_csv(os.path.join("data", file))
                ticker = file.split('_')[0]
                df["ticker"] = ticker
                df = df[["date", "open", "high", "low", "close", "volume", "ticker"]].drop_duplicates()
                df = compute_features(df)
                print(f"✅ Processed {file} (Ticker: {ticker})")
                combined.append(df)
            except Exception as e:
                print(f"❌ Error processing {file}: {e}")

    # Combine and save
    if combined:
        full_df = pd.concat(combined)
        full_df.to_csv("data/training_data/collated_training_data.csv", index=False)
        print(f"🎉 Dataset saved to: data/training_data/collated_training_data.csv")
    else:
        print("⚠️ No data processed.")


if __name__ == "__main__":
    prepare_dataset()
