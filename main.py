import requests

weather_codes = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Dense Drizzle",
    61: "Light Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    71: "Light Snow",
    73: "Moderate Snow",
    75: "Heavy Snow",
    80: "Light Rain Showers",
    81: "Moderate Rain Showers",
    82: "Violent Rain Showers",
    95: "Thunderstorm"
}

while True:

    city = input("\nEnter city name: ")

    if not city.strip():
        print("Please enter a city name.")
        continue

    try:
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
            "countryCode": "IN"
        }
        geo_response = requests.get(
            geo_url,
            params=geo_params,
            timeout=10
        )

        geo_response.raise_for_status()

        geo_data = geo_response.json()

        if "results" not in geo_data:
            print("City not found.")
            continue

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,weather_code",
            "daily": "temperature_2m_max,temperature_2m_min,weather_code",
            "forecast_days": 5,
            "temperature_unit": "celsius",
            "wind_speed_unit": "kmh",
            "timezone": "auto"
        }

        weather_response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10
        )

        weather_response.raise_for_status()

        weather_data = weather_response.json()

        current = weather_data["current"]

        condition = weather_codes.get(
            current["weather_code"],
            "Unknown"
        )

        print("\n" + "=" * 40)
        print("             WEATHER")
        print("=" * 40)
        print(f"City: {location['name']}")
        print(f"Country: {location['country']}")
        print(f"Condition: {condition}")
        print(f"Temperature: {current['temperature_2m']} °C")
        print(f"Feels Like: {current['apparent_temperature']} °C")
        print(f"Humidity: {current['relative_humidity_2m']}%")
        print(f"Wind Speed: {current['wind_speed_10m']} km/h")

        daily = weather_data["daily"]

        print("\n" + "=" * 40)
        print("          5-DAY FORECAST")
        print("=" * 40)

        for i in range(5):
            date = daily["time"][i]
            max_temp = daily["temperature_2m_max"][i]
            min_temp = daily["temperature_2m_min"][i]
            code = daily["weather_code"][i]

            condition = weather_codes.get(code, "Unknown")

            print(f"\n{date}")
            print(f"Condition: {condition}")
            print(f"Max: {max_temp} °C")
            print(f"Min: {min_temp} °C")

    except requests.exceptions.RequestException:
        print("Unable to connect to the weather service.")

    again = input("\nSearch another city? (y/n): ")

    if again.lower() != "y":
        print("Goodbye!")
        break