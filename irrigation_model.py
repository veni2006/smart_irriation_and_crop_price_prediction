import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("crop_recommendation.csv")

# -----------------------------
# Create Irrigation Target
# 1 = Need irrigation
# 0 = No irrigation
# -----------------------------
df["irrigation"] = (
    (df["rainfall"] < 150) &
    (df["humidity"] < 80) &
    (df["temperature"] > 25)
).astype(int)

# -----------------------------
# Encode Crop Labels
# -----------------------------
encoder = LabelEncoder()
df["label"] = encoder.fit_transform(df["label"])

# -----------------------------
# Features / Target
# -----------------------------
X = df[["temperature", "humidity", "ph", "rainfall", "label"]]
y = df["irrigation"]

# -----------------------------
# Train Model
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# Water Level Logic
# -----------------------------
def water_level(rainfall):
    if rainfall < 100:
        return "High Water Needed"
    elif rainfall < 180:
        return "Medium Water Needed"
    else:
        return "Low Water Needed"

# -----------------------------
# Prediction Function
# -----------------------------
def predict_irrigation(temp, humidity, ph, rainfall, crop_code):
    input_data = pd.DataFrame([{
        "temperature": temp,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall,
        "label": crop_code
    }])

    result = model.predict(input_data)[0]

    if result == 1:
        return "Irrigation Needed", water_level(rainfall)
    else:
        return "No Irrigation Needed", "No Water Required"