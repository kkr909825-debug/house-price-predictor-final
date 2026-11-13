import pandas as pd
from config import CITY_FILES, AMENITY_COLUMNS


def load_data():
    all_cities = []

    for city, path in CITY_FILES.items():
        data = pd.read_csv(path)
        data["city"] = city

        data = data.rename(columns={
            "Price": "price",
            "Area": "area_sqft",
            "Location": "location",
            "No. of Bedrooms": "bedrooms",
            "Resale": "resale",
        })
        data = data.rename(columns=AMENITY_COLUMNS)

        for name in AMENITY_COLUMNS.values():
            data[name] = data[name].replace(9, 0)

        data["location"] = data["location"].str.strip()
        data = data[(data["price"] > 0) & (data["area_sqft"] > 0)]
        data = data.drop_duplicates()
        all_cities.append(data)

    final = pd.concat(all_cities, ignore_index=True)
    final = remove_wrong_prices(final)
    return final


def remove_wrong_prices(data):
    data = data.copy()
    data["price_per_sqft"] = data["price"] / data["area_sqft"]

    group = data.groupby(["city", "location"])["price_per_sqft"]
    data["middle_rate"] = group.transform("median")
    data["listings"] = group.transform("size")

    data = data[data["listings"] >= 3]
    data = data[data["price_per_sqft"] >= data["middle_rate"] * 0.6]
    data = data[data["price_per_sqft"] <= data["middle_rate"] * 1.6]

    data = data.drop(columns=["price_per_sqft", "middle_rate", "listings"])
    return data.reset_index(drop=True)
