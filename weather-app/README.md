# Weather App

A command-line weather app that fetches real-time weather data using OpenWeatherMap API.

## Setup

1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Copy `.env.example` to `.env` and add your API key
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python weather.py`

## Features

- Search weather by city name
- Shows temperature, humidity, wind speed, and conditions
- Error handling for network issues and invalid cities
- Metric units (Celsius, m/s)
