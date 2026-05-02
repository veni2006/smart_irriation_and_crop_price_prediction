import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("commodity_prices.csv")

# -----------------------------
# Convert Date
# -----------------------------
df["Arrival_Date"] = pd.to_datetime(df["Arrival_Date"], dayfirst=True)

df["Day"] = df["Arrival_Date"].dt.day
df["Month"] = df["Arrival_Date"].dt.month
df["Year"] = df["Arrival_Date"].dt.year

# -----------------------------
# Encode Text Columns
# -----------------------------
text_cols = [
    "State",
    "District",
    "Market",
    "Commodity",
    "Variety",
    "Grade"
]

encoders = {}

for col in text_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    encoders[col] = le

# -----------------------------
# Features / Target
# -----------------------------
X = df[
    [
        "State",
        "District",
        "Market",
        "Commodity",
        "Variety",
        "Grade",
        "Day",
        "Month",
        "Year",
        "Min Price",
        "Max Price"
    ]
]

y = df["Modal Price"]

# -----------------------------
# Train Model
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# Prediction Function
# -----------------------------
def predict_price(
    state,
    district,
    market,
    commodity,
    variety,
    grade,
    day,
    month,
    year,
    min_price,
    max_price
):
    data = pd.DataFrame([{
        "State": state,
        "District": district,
        "Market": market,
        "Commodity": commodity,
        "Variety": variety,
        "Grade": grade,
        "Day": day,
        "Month": month,
        "Year": year,
        "Min Price": min_price,
        "Max Price": max_price
    }])

    return round(model.predict(data)[0], 2)