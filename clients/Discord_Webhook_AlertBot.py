import requests
import time
import os
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook, DiscordEmbed

load_dotenv()

FLASK_URL_API = "http://127.0.0.1:5000"

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

condition_images = {
    "Sunny": "https://cdn-icons-png.flaticon.com/512/3222/3222800.png",
    "Partly cloudy": "https://cdn-icons-png.flaticon.com/512/3222/3222792.png",
    "Light rain shower": "https://cdn-icons-png.flaticon.com/512/4150/4150897.png",
    "Patchy rain possible": "https://cdn-icons-png.flaticon.com/512/1146/1146858.png",
    "Cloudy": "https://cdn-icons-png.flaticon.com/512/3222/3222796.png"
}

def send_weather_alert():
    data = requests.get(f"{FLASK_URL_API}/current_weather").json()

    if data:
        response = requests.post(f"{FLASK_URL_API}/predict", json=data)
        if response.status_code != 200:
            print("Error from FlaskAPI:", response.text)
            return
        
        result = response.json()
        condition = result.get("predicted_condition", "Unknown")

        image_url = condition_images.get(condition, "https://cdn-icons-png.flaticon.com/512/414/414825.png")

        content_message = "@everyone 🌦️ **Weather Alert Update!**"

        embed = DiscordEmbed(
        title=f"Predicted Condition: {condition}",
        description="Latest simulated IoT weather reading:",
        color=0x00BFFF
    )
        
    details = "\n".join([
        f"🌡️ Temp: {data['temp_c']} °C",
        f"💧 Humidity: {data['humidity']} %",
        f"☁️ Cloud: {data['cloud']} %",
        f"📊 Pressure: {data['pressure_mb']} mb",
        f"🌬️ Wind: {data['wind_kph']} kph {data['wind_dir']}",
        f"☀️ Daytime: {'Yes' if data['is_day'] else 'No'}",
        f"🔆 UV Index: {data['uv']}"
    ])
    embed.add_embed_field(name="📋 Input Data", value=details, inline=True)

    embed.set_thumbnail(url=image_url)

    embed.set_footer(text="Smart Weather Alert Prediction System")

    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=content_message)
    webhook.add_embed(embed)
    response = webhook.execute()

    print(f"✅ Sent alert: {condition}")

while True:
    send_weather_alert()
    time.sleep(10)
