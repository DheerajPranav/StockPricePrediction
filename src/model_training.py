# src/model_training.py

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import numpy as np
import os


def evaluate_regression(y_true, y_pred, model_name="Model"):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)

    print(f"\n📊 Evaluation Metrics for {model_name}")
    print(f"🔢 MAE (Mean Absolute Error): {mae:.4f}")
    print(f"📉 MSE (Mean Squared Error): {mse:.4f}")
    print(f"📈 RMSE (Root Mean Squared Error): {rmse:.4f}")
    print(f"🎯 R² Score: {r2:.4f}")


def train_and_save_model():
    print(f"II. Model Building started...")

    # Load the prepared dataset
    df = pd.read_csv("data/training_data/collated_training_data.csv")

    # Define features and target
    features = ["return", "ma5", "ma10", "ma20", "vol_chg", "volatility", "rsi", "macd", "momentum"]
    target_col = "target"

    # Drop rows with any missing values in features or target
    df = df.dropna(subset=features + [target_col])

    # Create X and y
    X = df[features]
    y = df[target_col]

    # Train/test split (no shuffle for time-series style data)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False, random_state=42)

    # Initialize and train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    print("✅ Model Training Done.")

    # Evaluate
    y_pred = model.predict(X_test)
    evaluate_regression(y_test, y_pred, model_name="Random Forest Regressor")

    # Save model
    MODEL_DIR = 'models'
    MODEL_PATH = os.path.join(MODEL_DIR, 'rf_regressor.pkl')
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"📦 Saved the model to {MODEL_PATH}")


# Example to run
if __name__ == "__main__":
    train_and_save_model()
