"""
Weather App - fetches current weather data from OpenWeatherMap API
Uses requests library and displays formatted weather information
"""

import os
import sys
import requests
from dotenv import load_dotenv


def load_api_key():
    """Load the API key from .env file"""
    load_dotenv()
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        print("Error: WEATHER_API_KEY not found in .env file")
        print("Please create a .env file with your API key")
        print("See .env.example for reference")
        sys.exit(1)
    return api_key


def get_weather(city, api_key):
    """Fetch weather data from OpenWeatherMap API for a given city"""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the weather service")
        print("Please check your internet connection")
        return None
    except requests.exceptions.Timeout:
        print("Error: Request timed out. Try again later")
        return None
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f"Error: City '{city}' not found")
        elif response.status_code == 401:
            print("Error: Invalid API key")
        else:
            print(f"Error: HTTP {response.status_code} - {e}")
        return None


def display_weather(data):
    """Display the weather data in a nice formatted way"""
    city_name = data["name"]
    country = data["sys"]["country"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"]
    wind_speed = data["wind"]["speed"]

    print("\n" + "=" * 40)
    print(f"  Weather in {city_name}, {country}")
    print("=" * 40)
    print(f"  Temperature:  {temp}°C")
    print(f"  Feels like:   {feels_like}°C")
    print(f"  Humidity:     {humidity}%")
    print(f"  Conditions:   {description.title()}")
    print(f"  Wind speed:   {wind_speed} m/s")
    print("=" * 40 + "\n")


def main():
    """Main function - gets user input and displays weather"""
    print("\n--- Weather App ---\n")
    api_key = load_api_key()

    while True:
        city = input("Enter city name (or 'quit' to exit): ").strip()

        if city.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        if not city:
            print("Please enter a valid city name")
            continue

        weather_data = get_weather(city, api_key)
        if weather_data:
            display_weather(weather_data)


if __name__ == "__main__":
    main()
