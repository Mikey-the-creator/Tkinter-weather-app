import os
import tkinter as tk
from tkinter import font, messagebox
from dotenv import load_dotenv
from gif import AnimatedGIF
from geo_locator import GeoLocator
from weather import WeatherFetcher


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Weather")
        self.root.geometry("400x600")
        self.root.configure(bg="#2E2E2E")

        load_dotenv()
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            messagebox.showerror("Error", "API Key not found. Please check your .env file.")
            root.destroy()
            return

        self.geolocator = GeoLocator(api_key)
        self.weather_fetcher = WeatherFetcher(api_key)
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.weather_font = font.Font(family="Helvetica", size=36, weight="bold")
        self.desc_font = font.Font(family="Helvetica", size=14)
        self.text_color = "#FFFFFF"
        self.weather_gif_map = {
            "Thunderstorm": "thunderstorm.gif", "Drizzle": "drizzle.gif",
            "Rain": "rain.gif", "Snow": "snow.gif", "Mist": "mist.gif",
            "Smoke": "smoke.gif", "Haze": "haze.gif", "Dust": "dust.gif",
            "Fog": "fog.gif", "Sand": "sand.gif", "Ash": "ash.gif",
            "Squall": "squall.gif", "Tornado": "tornado.gif",
            "Clear": "clear.gif", "Clouds": "clouds.gif"
        }
        self._create_widgets()
        self.update_weather(self.location_entry.get())

    def _create_widgets(self):
        search_frame = tk.Frame(self.root, bg=self.root['bg'])
        search_frame.pack(pady=10, fill=tk.X, padx=20)

        self.location_entry = tk.Entry(search_frame, font=self.desc_font, justify='center', bg="#555555",
                                       fg=self.text_color, insertbackground=self.text_color)
        self.location_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, ipady=5, padx=(0, 5))
        self.location_entry.insert(0, "Lagos")

        search_button = tk.Button(search_frame, text="Search", font=self.desc_font, command=self.search_weather,
                                  bg="#555555", fg=self.text_color, activebackground="#777777")
        search_button.pack(side=tk.RIGHT)
        self.root.bind('<Return>', self.search_weather)

        self.location_label = tk.Label(self.root, text="Loading...", font=self.title_font, bg=self.root['bg'],
                                       fg=self.text_color)
        self.location_label.pack(pady=15)

        self.weather_label = tk.Label(self.root, text="", font=self.weather_font, bg=self.root['bg'],
                                      fg=self.text_color)
        self.weather_label.pack(pady=10)

        self.desc_label = tk.Label(self.root, text="", font=self.desc_font, bg=self.root['bg'], fg=self.text_color)
        self.desc_label.pack(pady=10)

        self.gif_label = None

    def search_weather(self, event=None):
        location = self.location_entry.get()
        if location:
            self.update_weather(location)
        else:
            messagebox.showwarning("Input Error", "Please enter a city name.")

    def update_weather(self, location):
        coords = self.geolocator.get_coords(location)
        if "error" in coords:
            self._display_error(coords["error"])
            return

        weather_data = self.weather_fetcher.fetch_by_coords(coords["lat"], coords["lon"])
        if "error" in weather_data:
            self._display_error(weather_data["error"])
            return

        self._update_ui(weather_data)

    def _display_error(self, message):
        self.location_label.config(text="Error")
        self.weather_label.config(text=message)
        self.desc_label.config(text="")
        if self.gif_label:
            self.gif_label.pack_forget()

    def _update_ui(self, data):
        self.location_label.config(text=data["location"])
        self.weather_label.config(text=data["temp"])
        self.desc_label.config(text=f"{data['main']} ({data['description']})")

        gif_file = os.path.join("assets", self.weather_gif_map.get(data["main"], "clear.gif"))

        if self.gif_label:
            self.gif_label.destroy()

        self.gif_label = AnimatedGIF(self.root, path=gif_file, bg=self.root['bg'])
        self.gif_label.pack(pady=20)
        self.gif_label.start_animation()


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
