from flask import Flask, request, jsonify, render_template_string
import joblib
import os
import pandas as pd

app = Flask(__name__)

# Load model and dataset
model = joblib.load(os.path.join(os.path.dirname(__file__), "models", "rf_regressor.pkl"))
data_path = os.path.join(os.path.dirname(__file__), "data", "training_data", "collated_training_data.csv")
full_data = pd.read_csv(data_path, parse_dates=["date"])

# Define feature columns
FEATURES = ["return", "ma5", "ma10", "ma20", "vol_chg", "volatility", "rsi", "macd", "momentum"]

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Stock Price Prediction</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f4f4f4; }
        .container { background: white; padding: 20px 30px; border-radius: 12px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); width: 400px; margin: auto; }
        h2 { color: #333; }
        input, button {
            width: 100%;
            padding: 10px;
            margin: 8px 0 15px;
            border: 1px solid #ccc;
            border-radius: 6px;
        }
        button {
            background: #007BFF;
            color: white;
            font-weight: bold;
            border: none;
            cursor: pointer;
        }
        .result {
            background: #e0ffe0;
            padding: 10px;
            border: 1px solid #00aa00;
            border-radius: 8px;
        }
        .error {
            background: #ffe0e0;
            padding: 10px;
            border: 1px solid #cc0000;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Predict Next Day Stock Price</h2>
        <form method="POST">
            <label>Ticker:</label>
            <input name="ticker" placeholder="e.g. AAPL" required>
            <label>Date (optional):</label>
            <input name="date" type="date">
            <button type="submit">Predict</button>
        </form>
        {% if prediction %}
            <div class="result">
                <strong>Ticker:</strong> {{ ticker }}<br>
                <strong>Base Date:</strong> {{ date }}<br>
                <strong>Last Close:</strong> ${{ last_close }}<br>
                <strong>Predicted Close (Next Day):</strong> ${{ predicted_price }}<br>
                <strong>Status:</strong> 📈 {{ status }}
            </div>
        {% endif %}
        {% if error %}
            <div class="error">
                <strong>Error:</strong> {{ error }}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    error = None
    date = None
    ticker = None
    predicted_price = None
    last_close = None
    status = None

    if request.method == "POST":
        try:
            ticker = request.form.get("ticker", "").upper()
            date_input = request.form.get("date")

            if not ticker:
                raise ValueError("Ticker is required.")

            df = full_data[full_data["ticker"] == ticker].copy()
            df = df.sort_values("date")

            if df.empty:
                raise ValueError(f"No data found for ticker: {ticker}")

            if date_input:
                date_parsed = pd.to_datetime(date_input)
                df = df[df["date"] <= date_parsed]
                if df.empty:
                    raise ValueError(f"No data available on or before {date_input} for ticker {ticker}")
            else:
                date_parsed = df["date"].max()

            base_row = df[df["date"] == date_parsed]
            if base_row.empty:
                base_row = df.iloc[[-1]]  # Fallback to last available row

            X_input = base_row[FEATURES]
            last_close = float(base_row["close"].values[0])

            predicted_price = float(model.predict(X_input)[0])
            status = "Up" if predicted_price > last_close else "Down"
            date = date_parsed.strftime("%Y-%m-%d")
            prediction = True

        except Exception as e:
            error = str(e)

    return render_template_string(
        HTML_TEMPLATE,
        prediction=prediction,
        ticker=ticker,
        date=date,
        predicted_price=f"{predicted_price:.2f}" if predicted_price else None,
        last_close=f"{last_close:.2f}" if last_close else None,
        status=status,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
