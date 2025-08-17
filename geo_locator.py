import requests

class GeoLocator:
    """
    Handles fetching geographic coordinates (latitude and longitude) for a given location
    using the OpenWeatherMap Geocoding API.
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/geo/1.0/direct"

    def get_coords(self, location_name):
        if not self.api_key:
            return {"error": "API Key not provided."}

        params = {
            "q": location_name,
            "limit": 1,
            "appid": self.api_key
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if not data:
                return {"error": f"Location '{location_name}' not found."}

            return {
                "lat": data[0]["lat"],
                "lon": data[0]["lon"]
            }
        except requests.exceptions.RequestException as e:
            return {"error": f"Network Error: {e}"}
        except (KeyError, IndexError):
            return {"error": "Error parsing geolocation response."}
