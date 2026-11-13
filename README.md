# House Price Predictor

A machine learning project that predicts house prices in six Indian cities
(Bangalore, Chennai, Delhi, Hyderabad, Kolkata, Mumbai) using a Flask website.

## Dataset
Housing data for six cities, one CSV file per city, kept in the `data` folder.
Each row has the price, area, location, number of bedrooms, resale status and
a list of facilities (1 = available, 0 = not available, 9 = not given).

The dataset does not have bathrooms, floors, age of the property or road
details, so those features are not used.

## How it works
1. `data_loader.py` reads the six CSV files and joins them together.
2. Facilities marked 9 (not given) are treated as 0.
3. Rows with a price per sq ft far away from the usual price in the same location are removed, because many of them are wrong entries.
4. `train_model.py` trains Linear Regression and Random Forest, compares the R2 scores and saves the better model.
5. `app.py` loads the saved model and gives the predicted price to the website.

## Run on your computer
```
pip install -r requirements.txt
python app.py
```
Then open http://localhost:5000 in the browser.

To train the model again: `python train_model.py`

## Files
| File | Use |
|---|---|
| app.py | Flask server and prediction API |
| train_model.py | trains and saves the model |
| data_loader.py | loads and cleans the data |
| config.py | list of cities, facilities and columns |
| templates/index.html | web page |
| static/style.css | design |
| static/app.js | sends the form to the server and shows the price |
