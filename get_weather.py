import openmeteo_requests
import geopy
import pandas as pd
import requests_cache
from retry_requests import retry
from promptflow.core import tool

@tool
def get_daily_dataframe(city_name, country_name) -> pd.DataFrame:
    #city_name = input("Enter the city name: ")
    #country_name = input("Enter the country name: ")

    geolocator = geopy.Nominatim(user_agent="my_app")
    location = f"{city_name}, {country_name}"
    location_obj = geolocator.geocode(location)
    if not location_obj:
        return None
    latitude = location_obj.latitude
    longitude = location_obj.longitude

    if not (latitude, longitude):
        print("Location not found.")
        exit()

    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ["weather_code", "sunrise", "sunset", "daylight_duration", "sunshine_duration", "temperature_2m_max", "temperature_2m_min", "precipitation_probability_max", "precipitation_hours"],
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_sunrise = daily.Variables(1).ValuesInt64AsNumpy()
    daily_sunset = daily.Variables(2).ValuesInt64AsNumpy()
    daily_daylight_duration = daily.Variables(3).ValuesAsNumpy()
    daily_sunshine_duration = daily.Variables(4).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(5).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(6).ValuesAsNumpy()
    daily_precipitation_probability_max = daily.Variables(7).ValuesAsNumpy()
    daily_precipitation_hours = daily.Variables(8).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}

    daily_data["weather_code"] = daily_weather_code
    daily_data["sunrise"] = daily_sunrise
    daily_data["sunset"] = daily_sunset
    daily_data["daylight_duration"] = daily_daylight_duration
    daily_data["sunshine_duration"] = daily_sunshine_duration
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["precipitation_probability_max"] = daily_precipitation_probability_max
    daily_data["precipitation_hours"] = daily_precipitation_hours

    daily_dataframe = pd.DataFrame(data = daily_data)
    return daily_dataframe
