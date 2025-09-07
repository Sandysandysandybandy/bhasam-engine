# This is the updated Python code, adapted to run on Render.
# It uses a lightweight web framework called Flask to create a web API.

import os
from flask import Flask, request, jsonify
import requests

# Initialize the Flask app.
app = Flask(__name__)

# IMPORTANT: This is your Alpha Vantage API key.
ALPHA_VANTAGE_API_KEY = "LU1020ACE39BLEGG"

# This defines the main endpoint for our API.
# The app will call this URL to get stock data.
@app.route('/get_stock_data', methods=['GET'])
def get_stock_data():
    try:
        ticker = request.args.get("ticker")

        if not ticker:
            return jsonify({"error": "Please provide a 'ticker' parameter."}), 400

        print(f"Received request for ticker: {ticker}")

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
            print(f"Alpha Vantage API Error: {data['Error Message']}")
            return jsonify({"error": data['Error Message']}), 404

        print(f"Successfully fetched data for {ticker}")
        return jsonify(data)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

# This is a simple health check endpoint to confirm the server is running.
@app.route('/')
def index():
    return "BHASAM Data Engine is running."