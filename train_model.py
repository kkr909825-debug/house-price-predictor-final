import json
import os
import joblib
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from config import ALL_COLUMNS, NUMBER_COLUMNS, TEXT_COLUMNS
from data_loader import load_data

MODEL_FILE = "model/house_price_model.joblib"
INFO_FILE = "model/model_info.json"


def make_pipeline(model):
    prepare = ColumnTransformer([
        ("text", OneHotEncoder(handle_unknown="ignore"), TEXT_COLUMNS),
        ("numbers", "passthrough", NUMBER_COLUMNS),
    ])
    return Pipeline([("prepare", prepare), ("model", model)])


def train():
    os.makedirs("model", exist_ok=True)
    data = load_data()
    print("Total rows:", len(data))

    x = data[ALL_COLUMNS]
    y = np.log(data["price"])

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=100, min_samples_leaf=2, n_jobs=-1, random_state=42),
    }

    best_name = ""
    best_score = -1
    best_pipeline = None
    scores = {}

    for name, model in models.items():
        pipeline = make_pipeline(model)
        pipeline.fit(x_train, y_train)
        predicted = pipeline.predict(x_test)
        score = r2_score(y_test, predicted)
        scores[name] = round(float(score), 3)
        print(name, "R2 score:", round(score, 3))
        if score > best_score:
            best_score = score
            best_name = name
            best_pipeline = pipeline

    predicted_price = np.exp(best_pipeline.predict(x_test))
    real_price = np.exp(y_test)
    mae = mean_absolute_error(real_price, predicted_price)
    error_percent = float(np.mean(np.abs(real_price - predicted_price) / real_price) * 100)

    info = {
        "best_model": best_name,
        "r2_score": round(float(best_score), 3),
        "average_error_lakhs": round(float(mae) / 100000, 2),
        "average_error_percent": round(error_percent, 1),
        "all_scores": scores,
        "rows_used": int(len(data)),
    }

    cities = {}
    for city in sorted(data["city"].unique()):
        cities[city] = sorted(data[data["city"] == city]["location"].unique().tolist())
    info["cities"] = cities

    joblib.dump(best_pipeline, MODEL_FILE, compress=3)
    with open(INFO_FILE, "w") as file:
        json.dump(info, file, indent=2)

    print("Best model:", best_name)
    print("Average error:", info["average_error_percent"], "%")
    return info


if __name__ == "__main__":
    train()
