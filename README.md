
# Stock Price Movement Prediction

##  Overview
This project predicts the next day's closing price of a stock based on historical data and relevant features.

##  Project Structure

- `main.py`: Orchestrates the full pipeline.
- `app.py`: Flask API to serve predictions.
- `src/`: Contains the ingestion, processing, and training scripts.
  - `data_ingestion.py`: Scripts for fetching and storing data.
  - `data_processing.py`: Scripts for cleaning and preparing data.
  - `model_training.py`: Scripts for training the machine learning model.
- `models/`: Stores the trained machine learning models (e.g., pickle files).
- `noteooks/`: we have our data prepared , EDA done & model trained in a detailed way here.
- `data/`: Contains any raw or processed data files (e.g., CSV files).
  - `collated_training_data.csv`: Example of data used for training.
  
- `Dockerfile`: Instructions for building a Docker image for the application.
- `README.md`: This file, providing project information and instructions.
- `requirements.txt`: Lists the Python dependencies required for the project.
## Note:

If we want to dive deeper into the model, data analysis, or experiment with different features and techniques, refer to the Jupyter notebooks (.ipynb files) for detailed insights and exploration.

```bash
1_Data_Ingestion.ipynb
2_Data_Prep.ipynb
3_Model_Building.ipynb
```
##  Setup Instructions

### 1. Local Setup
```bash
git clone https://github.com/DheerajPranav/StockPricePrediction.git
cd StockPricePrediction
```

#### Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate   # On Windows
```

#### Install dependencies:
```bash
pip install -r requirements.txt
```

#### Run the main pipeline (optional, for data processing and model training):
```bash
python main.py

# Run the Flask API:
python app.py
```


### 2. Docker Setup

#### Build the Docker image:
Navigate to the project root directory (where the Dockerfile is located) and run:

```bash
docker build -t stock-predictor
```
 Run the Docker container:

```bash
docker run -p 5000:5000 stock-predictor
```
The API will be accessible at http://localhost:5000.

## 🧪 API Testing Instructions

The API provides a `/predict` endpoint that accepts POST requests with JSON data containing the features for prediction.

#### Example using `curl`:

```bash
curl -X POST \
  http://localhost:5000/predict \
  -H 'Content-Type: application/json' \
  -d '{"return":0.01,"ma5":145.6,"ma10":146.2,"ma20":144.2,"vol_chg":0.05,"volatility":0.02,"rsi":60,"macd":0.1,"momentum":0.05}'
```

#### Expected Response:

The API will return a JSON response indicating the predicted stock price for the next day and whether the price is expected to go up or down.

#### Example response:
```bash
{
  "ticker": "AAPL",
  "base_date": "2025-04-12",
  "last_close": 145.30,
  "predicted_close": 146.10,
  "status": "Up"
}
```

## Feature Choices and Model Selection
For this project, we’ve chosen a set of technical indicators as input features for predicting the next day's closing stock price. These features were selected based on their ability to capture important patterns and trends in stock price movements:

- Moving Averages (MA5, MA10, MA20): These indicators help smooth out stock price fluctuations and highlight the underlying trend. The short-term (MA5), mid-term (MA10), and long-term (MA20) averages are used to capture different aspects of price behavior. 
- Volume Change (vol_chg): An increase in volume often accompanies significant price movements, signaling strength in a trend. 
- Volatility: Represents how much the stock price fluctuates, which can be a useful predictor for price movement. 
- Relative Strength Index (RSI): A momentum oscillator used to identify whether a stock is overbought or oversold, which can help in predicting price reversals. 
- MACD (Moving Average Convergence Divergence): A trend-following momentum indicator that shows the relationship between two moving averages of a stock's price. 
- Momentum: Captures the speed and direction of price movement, indicating the likelihood of future movement continuation.


## Model Selection:
> We’ve chosen a Random Forest Regressor for this project due to its robustness and ability to handle non-linear relationships. It performs well even when there are noisy data points and can capture complex interactions between the features. Additionally, it offers feature importance scores, which allow us to understand which indicators have the most impact on predictions.

> Future versions could explore more advanced models like LSTM (Long Short-Term Memory networks), which are better suited for time-series data, and experiment with additional technical indicators.

## Assumptions Made During Development
- Data Availability: The project assumes that historical stock price data, including prices (open, close, high, low) and volume, is readily available and can be used to generate the required features for training the model. 
- Feature Relevance: The selected features (moving averages, volume change, volatility, etc.) are based on widely-used technical analysis indicators. We assume that these indicators hold predictive power for short-term stock price movements, though further validation may be needed through exploratory data analysis and model evaluation. 
- Stationarity of Data: Stock price data is inherently non-stationary, meaning it has trends and patterns that change over time. While the moving averages help smooth the data, we have not explicitly addressed the stationarity issue, which may be important for long-term price predictions. 
- Simplified Prediction Task: The current version of the project focuses on predicting the direction (up or down) or the next day's closing price, rather than the exact price movement. The model's objective is simplified to a regression task for predicting the next day’s closing price. 
- Evaluation Metrics: The model’s performance is evaluated based on standard regression metrics, such as Mean Squared Error (MSE) or Mean Absolute Error (MAE), to measure how well the predictions align with the actual prices. Future iterations could consider additional performance measures based on business requirements.
