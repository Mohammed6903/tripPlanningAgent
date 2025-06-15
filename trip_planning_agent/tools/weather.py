import requests
import os

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_lat_lon(city_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city_name, "format": "json", "limit": 1}
    response = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"})
    data = response.json()
    if data:
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        print(f"{city_name}: Latitude={lat}, Longitude={lon}")
        return lat, lon
    else:
        print(f"City '{city_name}' not found!")
        return None, None


def get_weather(city: str) -> dict:
    """
    Retrieves the current weather for a specified city.

    Args:
        city (str): The name of the city to get the weather for.

    Retruns:
        dict: status and result or error message.
    """
    try:
        if not OPENWEATHER_API_KEY:
            print("OPENWEATHER_API_KEY is not set.")
        lat, lon = get_lat_lon(city)

        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
        )

        return {
            "status": "success",
            "report": (
                f"""
                    Current weather in {city}: {response.json().get("main", {})}
                """
            ),
        }

    except requests.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to retrieve weather data: {str(e)}",
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"An unexpected error occurred: {str(e)}",
        }
