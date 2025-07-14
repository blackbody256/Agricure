from dotenv import load_dotenv
import requests
import os
from typing import Dict, List, Optional

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if API_KEY:
    API_KEY = API_KEY.strip()

# Base URLs for OpenWeatherMap API
BASE_GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"
BASE_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
BASE_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

class WeatherClient:
    def __init__(self):
        if not API_KEY:
            print("Warning: OPENWEATHER_API_KEY not found in environment variables")
            print("Please add your API key to the .env file")
            # Don't raise an error immediately - let the app start
            self.api_key = None
        else:
            self.api_key = API_KEY
    
    def _check_api_key(self):
        """Check if API key is available before making requests"""
        if not self.api_key:
            raise ValueError("OpenWeather API key is not configured. Please set OPENWEATHER_API_KEY in your .env file")
    
    def get_coordinates_by_city(self, city_name: str, country_code: str = "UG") -> Optional[Dict]:
        """Get latitude and longitude for a city name"""
        self._check_api_key()
        
        try:
            params = {
                'q': f"{city_name},{country_code}" if country_code else city_name,
                'limit': 1,
                'appid': self.api_key
            }
            
            response = requests.get(BASE_GEO_URL, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data:
                return {
                    'lat': data[0]['lat'],
                    'lon': data[0]['lon'],
                    'name': data[0]['name'],
                    'country': data[0]['country']
                }
            return None
        except Exception as e:
            print(f"Error getting coordinates: {e}")
            return None
    
    def get_weather_by_coordinates(self, lat: float, lon: float) -> Optional[Dict]:
        """Get current weather data using latitude and longitude"""
        self._check_api_key()
        
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(BASE_WEATHER_URL, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            weather_info = {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'visibility': data.get('visibility', 0) / 1000,
                'location': data['name'],
                'country': data['sys']['country'],
                'feels_like': data['main']['feels_like'],
                'cloudiness': data['clouds']['all'],
                'sunrise': data['sys']['sunrise'],
                'sunset': data['sys']['sunset']
            }
            
            return weather_info
        except Exception as e:
            print(f"Error getting weather data: {e}")
            return None
    
    def get_weather_forecast(self, lat: float, lon: float, days: int = 5) -> Optional[List]:
        """Get weather forecast for specified days"""
        self._check_api_key()
        
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(BASE_FORECAST_URL, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            forecast_list = []
            for item in data['list'][:days * 8]:
                forecast_list.append({
                    'datetime': item['dt_txt'],
                    'temperature': item['main']['temp'],
                    'humidity': item['main']['humidity'],
                    'description': item['weather'][0]['description'],
                    'wind_speed': item['wind']['speed'],
                    'feels_like': item['main']['feels_like'],
                    'pressure': item['main']['pressure'],
                    'cloudiness': item['clouds']['all']
                })
            
            return forecast_list
        except Exception as e:
            print(f"Error getting forecast: {e}")
            return None
    
    def get_weather_for_gemini(self, lat: float, lon: float) -> List:
        """Get weather data formatted for Gemini AI input"""
        weather_data = self.get_weather_by_coordinates(lat, lon)
        
        if not weather_data:
            return [None, None, None, None, None, None, None]
        
        return [
            weather_data['temperature'],
            weather_data['humidity'],
            weather_data['pressure'],
            weather_data['wind_speed'],
            weather_data['visibility'],
            weather_data['description'],
            weather_data['cloudiness']
        ]
    
    def get_weather_by_city_for_gemini(self, city_name: str, country_code: str = "UG") -> List:
        """Get weather data by city name, formatted for Gemini AI"""
        coords = self.get_coordinates_by_city(city_name, country_code)
        if not coords:
            return [None, None, None, None, None, None, None]
        
        return self.get_weather_for_gemini(coords['lat'], coords['lon'])

# Convenience functions for backward compatibility
def get_coordinates_by_city(city_name: str, country_code: str = None) -> Optional[Dict]:
    try:
        client = WeatherClient()
        return client.get_coordinates_by_city(city_name, country_code or "UG")
    except ValueError as e:
        print(f"Weather API Error: {e}")
        return None

def get_weather_by_coordinates(lat: float, lon: float) -> Optional[Dict]:
    try:
        client = WeatherClient()
        return client.get_weather_by_coordinates(lat, lon)
    except ValueError as e:
        print(f"Weather API Error: {e}")
        return None

def get_weather_forecast(lat: float, lon: float, days: int = 5) -> Optional[List]:
    try:
        client = WeatherClient()
        return client.get_weather_forecast(lat, lon, days)
    except ValueError as e:
        print(f"Weather API Error: {e}")
        return None