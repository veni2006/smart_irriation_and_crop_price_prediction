from flask import Flask, render_template, request
from irrigation_model import predict_irrigation
from price_model import predict_price
import random

app = Flask(__name__)

crop_dict = {
    "Rice": 20,
    "Wheat": 21,
    "Maize": 12,
    "Cotton": 7,
    "Sugarcane": 18,
    "Barley": 3,
    "Millet": 14
}

@app.route("/", methods=["GET", "POST"])
def home():

    irrigation_result = None
    water_result = None
    price_result = None
    future_price = None
    chart_values = []

    # Dashboard stats
    water_saved = random.randint(18, 35)
    profit_growth = random.randint(10, 25)
    yield_growth = random.randint(8, 20)

    rain_alerts = [
        "Light Rain Tomorrow",
        "Sunny Next 3 Days",
        "Heavy Rain Expected",
        "Cloudy Weather Ahead",
        "No Rain This Week"
    ]

    rain_alert = random.choice(rain_alerts)

    if request.method == "POST":

        # Irrigation
        if "irrigation_btn" in request.form:

            temp = float(request.form["temperature"])
            humidity = float(request.form["humidity"])
            ph = float(request.form["ph"])
            rainfall = float(request.form["rainfall"])

            crop_name = request.form["crop"]
            crop_code = crop_dict[crop_name]

            irrigation_result, water_result = predict_irrigation(
                temp, humidity, ph, rainfall, crop_code
            )

        # Price
        if "price_btn" in request.form:

            state = int(request.form["state"])
            district = int(request.form["district"])
            market = int(request.form["market"])
            commodity = int(request.form["commodity"])
            variety = int(request.form["variety"])
            grade = int(request.form["grade"])

            day = int(request.form["day"])
            month = int(request.form["month"])
            year = int(request.form["year"])

            min_price = float(request.form["min_price"])
            max_price = float(request.form["max_price"])

            price_result = predict_price(
                state, district, market,
                commodity, variety, grade,
                day, month, year,
                min_price, max_price
            )

            future_price = round(price_result * 1.05, 2)

            chart_values = [
                round(price_result * 0.92, 2),
                round(price_result * 0.97, 2),
                price_result,
                future_price
            ]

    return render_template(
        "index.html",
        irrigation_result=irrigation_result,
        water_result=water_result,
        price_result=price_result,
        future_price=future_price,
        chart_values=chart_values,
        crop_names=list(crop_dict.keys()),
        water_saved=water_saved,
        profit_growth=profit_growth,
        yield_growth=yield_growth,
        rain_alert=rain_alert
    )

if __name__ == "__main__":
    app.run(debug=True)