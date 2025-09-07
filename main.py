# This is the upgraded Python code, incorporating your suggestions.
# 1. Uses an environment variable for the API key (more secure).
# 2. Uses the logging module for better debugging.
# 3. Trims the data from Alpha Vantage to only the last 30 days (more efficient).

import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

# Set up proper logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# 1. Get the API key securely from an environment variable
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

@app.route('/get_stock_data', methods=['GET'])
def get_stock_data():
    """
    Fetches the last 30 days of time series data for a given stock ticker.
    """
    try:
        ticker = request.args.get("ticker")

        if not ticker:
            logger.warning("Request received without a ticker parameter.")
            return jsonify({"error": "Please provide a 'ticker' parameter."}), 400

        # Check if the API key is configured on the server
        if not ALPHA_VANTAGE_API_KEY:
            logger.error("ALPHA_VANTAGE_API_KEY environment variable is not set on the server.")
            return jsonify({"error": "Server is not configured with an API key."}), 500

        logger.info(f"Received request for ticker: {ticker}")

        url = (
            "https://www.alphavantage.co/query?"
            "function=TIME_SERIES_DAILY"
            f"&symbol={ticker}"
            f"&apikey={ALPHA_VANTAGE_API_KEY}"
        )

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "Error Message" in data:
            logger.error(f"Alpha Vantage API Error for {ticker}: {data['Error Message']}")
            return jsonify({"error": data['Error Message']}), 404
        
        # 2. Trim the data to the last 30 days for efficiency
        if "Time Series (Daily)" in data:
            trimmed_series = dict(list(data["Time Series (Daily)"].items())[:30])
            trimmed_data = {
                "Meta Data": data["Meta Data"],
                "Time Series (Daily)": trimmed_series
            }
            logger.info(f"Successfully fetched and trimmed data for {ticker}")
            return jsonify(trimmed_data)
        else:
             logger.error(f"No time series data found for {ticker} in response.")
             return jsonify({"error": "No time series data found."}), 404


    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from Alpha Vantage: {e}")
        return jsonify({"error": "Error communicating with the financial data provider."}), 500

    except Exception as e:
        logger.error(f"An unexpected server error occurred: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

@app.route('/')
def index():
    return "BHASAM Data Engine v2 is running."

