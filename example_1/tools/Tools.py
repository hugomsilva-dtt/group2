"""This class contains tools related to travel assistant agent."""

import os
import requests
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults

class Tools():
    def __init__(self):
        load_dotenv()
        self.weather_api_key = os.environ["WEATHER_API_KEY"]
        self.tavily_api_key = os.environ["TAVILY_API_KEY"]

    def get_weather_data(self, city: str) -> dict:
        """
        This function is used when you need to retrieve weather information for a specified city.

        Args:
            city (str): The city name for which to retrieve weather data.

        Returns:
            dict: A dictionary containing weather data like temperature and weather conditions.
        """
        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}"
        response = requests.get(api_url, params={"units": "metric"})
        response.raise_for_status()  # error handling
        data = response.json()
        return {
            "temperature": data['main']['temp'],
            "temperature_feels_like": data['main']['feels_like'],
            "temperature_min": data['main']['temp_min'],
            "temperature_max": data['main']['temp_max'],
            "main_condition": data['weather'][0]['main'],
            "condition_description": data['weather'][0]['description'],
        }
    
    def get_trending_attractions(self, city: str) -> dict:
        """
        This function is used when you need to retrieve trending attractions in a city.

        Args:
            city (str): The city name for which to retrieve trending attractions.

        Returns:
            dict: A dictionary containing trending attractions in the city.
        """
        
        search = TavilySearchResults(max_results=5)
        search_results = search.run(f"{city} trending attractions")
        return search_results
