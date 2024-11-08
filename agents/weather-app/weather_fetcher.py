import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import requests

class WeatherFetcher:
    def __init__(self, cache_expire=3600, retries=5, backoff_factor=0.2):
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('/tmp/.cache', expire_after=cache_expire)
        retry_session = retry(cache_session, retries=retries, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=retry_session)
        self.url = "https://api.open-meteo.com/v1/forecast"

    def get_coordinates_and_country(self, city_name):
        """Fetch the latitude, longitude, country, and country code for a given city name."""
        geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&format=json"
        response = requests.get(geocoding_url)
        data = response.json()

        if data['results']:
            result = data['results'][0]
            return {
                'city_name': result['name'],
                'latitude': result['latitude'],
                'longitude': result['longitude'],
                'country': result['country'],
                'country_code': result['country_code']
            }
        else:
            raise ValueError(f"City '{city_name}' not found.")

    def fetch_weather_data(self, city_name):
        """Fetch the weather data for a given city name."""
        location_info = self.get_coordinates_and_country(city_name)
        params = {
            "latitude": location_info['latitude'],
            "longitude": location_info['longitude'],
            "hourly": "temperature_2m,precipitation,wind_speed_10m,rain,cloud_cover,relative_humidity_2m",
            "models": "ecmwf_ifs025"
        }
        responses = self.openmeteo.weather_api(self.url, params=params)
        return responses[0], location_info

    def get_current_weather(self, city_name):
        """Get the current weather data for a given city name and return it as a Python dictionary."""
        response, location_info = self.fetch_weather_data(city_name)
        
        # Process hourly data
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()
        hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()
        hourly_rain = hourly.Variables(3).ValuesAsNumpy()
        hourly_cloud_cover = hourly.Variables(4).ValuesAsNumpy()
        hourly_relative_humidity_2m = hourly.Variables(5).ValuesAsNumpy()

        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            ),
            "temperature": hourly_temperature_2m,
            "precipitation": hourly_precipitation,
            "wind_speed": hourly_wind_speed_10m,
            "rain": hourly_rain,
            "cloud_cover": hourly_cloud_cover,
            "relative_humidity": hourly_relative_humidity_2m
        }

        hourly_dataframe = pd.DataFrame(data=hourly_data)
        current_weather = hourly_dataframe.iloc[-1].to_dict()
        
        # Add location info to the output
        current_weather['city'] = location_info['city_name']
        current_weather['country'] = location_info['country']
        current_weather['country_code'] = location_info['country_code']
        current_weather['latitude'] = location_info['latitude']
        current_weather['longitude'] = location_info['longitude']
        
        return current_weather  # Return as a Python dictionary