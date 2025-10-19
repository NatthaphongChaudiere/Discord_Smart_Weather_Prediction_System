from flask import Flask, jsonify, request
import pandas as pd
import random
import pickle
from datetime import datetime
from dotenv import load_dotenv

model = pickle.load(open("weather_prediction_model.pkl", "rb"))
le_wind = pickle.load(open("le_wind.pkl", "rb"))
le_condition = pickle.load(open("le_condition.pkl", "rb"))

load_dotenv()

app = Flask(__name__)

@app.route('/current_weather', methods = ["GET"])
def current_weather():
    weather_data = {
        "temp_c": round(random.uniform(24, 30), 1),
        "humidity": random.randint(50, 95),
        "cloud": random.randint(10, 100),
        "pressure_mb": random.randint(1005, 1012),
        "dewpoint_c": round(random.uniform(20, 25), 1),
        "wind_kph": round(random.uniform(2, 15), 1),
        "wind_dir": random.choice(["N", "NNE", "ESE", "WNW", "S", "SW"]),
        "is_day": random.choice([0, 1]),
        "uv": round(random.uniform(0, 10), 1)
    }

    return jsonify(weather_data)

@app.route('/predict', methods = ["POST"])
def predict():
    try:
        data = request.get_json()

        wind_dir_encoded = le_wind.transform([data['wind_dir']])[0]

        sample = pd.DataFrame([{
            'temp_c': data['temp_c'],
            'humidity': data['humidity'],
            'cloud': data['cloud'],
            'pressure_mb': data['pressure_mb'],
            'dewpoint_c': data['dewpoint_c'],
            'wind_kph': data['wind_kph'],
            'wind_dir': wind_dir_encoded,
            'is_day': data['is_day'],
            'uv': data['uv']
        }])

        # Make prediction
        prediction = model.predict(sample)[0]
        condition = le_condition.inverse_transform([prediction])[0]

        return jsonify({'predicted_condition': condition})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)