import requests

class WeatherFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def fetch_by_coords(self, lat, lon):
        if not self.api_key:
            return {"error": "API Key not provided."}

        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric"
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            return {
                "location": data["name"],
                "main": data["weather"][0]["main"],
                "description": data["weather"][0]["description"].title(),
                "temp": f"{data['main']['temp']:.0f}°C"
            }
        except requests.exceptions.RequestException as e:
            return {"error": f"Network Error: {e}"}
        except (KeyError, IndexError):
            return {"error": "Error parsing weather response."}
