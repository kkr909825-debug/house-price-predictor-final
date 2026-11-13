CITY_FILES = {
    "Bangalore": "data/Bangalore.csv",
    "Chennai": "data/Chennai.csv",
    "Delhi": "data/Delhi.csv",
    "Hyderabad": "data/Hyderabad.csv",
    "Kolkata": "data/Kolkata.csv",
    "Mumbai": "data/Mumbai.csv",
}

AMENITY_COLUMNS = {
    "CarParking": "parking",
    "LiftAvailable": "lift",
    "24X7Security": "security",
    "Gymnasium": "gym",
    "SwimmingPool": "pool",
    "PowerBackup": "power_backup",
    "ClubHouse": "club_house",
}

AMENITY_LABELS = {
    "parking": "Car parking",
    "lift": "Lift",
    "security": "24x7 security",
    "gym": "Gym",
    "pool": "Swimming pool",
    "power_backup": "Power backup",
    "club_house": "Club house",
}

NUMBER_COLUMNS = ["area_sqft", "bedrooms", "resale"] + list(AMENITY_COLUMNS.values())
TEXT_COLUMNS = ["city", "location"]
ALL_COLUMNS = NUMBER_COLUMNS + TEXT_COLUMNS
