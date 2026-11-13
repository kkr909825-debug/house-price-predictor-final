import json
import os
import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request

from config import AMENITY_LABELS, ALL_COLUMNS
from train_model import MODEL_FILE, INFO_FILE, train

app = Flask(__name__)

if not os.path.exists(MODEL_FILE):
    train()

model = joblib.load(MODEL_FILE)
with open(INFO_FILE) as file:
    info = json.load(file)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/options")
def options():
    return jsonify({
        "cities": info["cities"],
        "amenities": AMENITY_LABELS,
        "model": {
            "name": info["best_model"],
            "r2_score": info["r2_score"],
            "error_percent": info["average_error_percent"],
        },
    })


@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data received"}), 400

    city = data.get("city")
    location = data.get("location")
    if city not in info["cities"]:
        return jsonify({"error": "Please choose a city"}), 422
    if location not in info["cities"][city]:
        return jsonify({"error": "Please choose a location"}), 422

    try:
        area = float(data.get("area_sqft"))
        bedrooms = int(data.get("bedrooms"))
    except (TypeError, ValueError):
        return jsonify({"error": "Area and bedrooms must be numbers"}), 422

    if area < 200 or area > 10000:
        return jsonify({"error": "Area must be between 200 and 10000 sq ft"}), 422
    if bedrooms < 1 or bedrooms > 10:
        return jsonify({"error": "Bedrooms must be between 1 and 10"}), 422

    row = {
        "city": city,
        "location": location,
        "area_sqft": area,
        "bedrooms": bedrooms,
        "resale": 1 if data.get("resale") == "resale" else 0,
    }
    for name in AMENITY_LABELS:
        row[name] = 1 if data.get(name) else 0

    table = pd.DataFrame([row])[ALL_COLUMNS]
    price = float(np.exp(model.predict(table)[0]))

    error = info["average_error_percent"] / 100
    return jsonify({
        "price": round(price, -3),
        "low": round(price * (1 - error), -3),
        "high": round(price * (1 + error), -3),
        "price_per_sqft": round(price / area),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
