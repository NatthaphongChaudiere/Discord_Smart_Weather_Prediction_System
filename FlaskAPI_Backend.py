from flask import Flask, jsonify, request
import pandas as pd
import random
import pickle
import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

model = pickle.load(open("weather_prediction_model.pkl", "rb"))
le_wind = pickle.load(open("le_wind.pkl", "rb"))
le_condition = pickle.load(open("le_condition.pkl", "rb"))

GEMINI_APIKEY = os.getenv("GEMINI_APIKEY")
client = genai.Client(api_key=GEMINI_APIKEY)

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

        prompt = f'''

            Gemini, so your duty is to give detail short feedback (advice, cautious, suggestion, activity or etc.) on what to do when the weather is like
            the json string format I'm provide below 
            (Only answer with letter like a people giving advice, u don't need to put **Suggestion** or any sign at the front):

        '''

        # Ai-Suggestion
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents= f"{prompt}\n{json.dumps(data)}\nThe weather is predict to be: {condition}"
        )

        return jsonify({'predicted_condition': condition, 'ai_suggestion': response.text})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)