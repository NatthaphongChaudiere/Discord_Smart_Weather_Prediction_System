import requests
import pandas as pd
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Weather API Setup
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def fetch_history_weather():

    historical_weather_data = {
        "temp_c": [],
        "humidity": [],
        "cloud": [],
        "pressure_mb": [],
        "dewpoint_c": [],
        "wind_kph": [],
        "wind_dir": [],
        "is_day": [],
        "uv": [],
        "condition": []
    }

    cities = ["Bangkok"]
    
    for city in cities:
        for day in range(1, 7):
            current_day = datetime.now()
            current_day = current_day - timedelta(day)
            current_day = current_day.strftime('%Y-%m-%d')
            url = f"http://api.weatherapi.com/v1/history.json?key={WEATHER_API_KEY}&q={city}&dt={current_day}"
            response = requests.get(url).json()

            for hour in range(0, 24):
                for key in historical_weather_data.keys():
                    if key == "condition":
                        historical_weather_data[key].append(response["forecast"]["forecastday"][0]["hour"][hour]["condition"]["text"])
                    else:
                        historical_weather_data[key].append(response["forecast"]["forecastday"][0]["hour"][hour][key])

    df = pd.DataFrame(historical_weather_data)
    df.to_excel("Historical_Weather_Data.xlsx", index=False)

    print(f"Successfully, saved alldatas.")

fetch_history_weather()