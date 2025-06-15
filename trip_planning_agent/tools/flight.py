import os
import requests

AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY")
AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET")


def get_bearer_token() -> str | None:
    """Fetch bearer token from Amadeus API."""
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": AMADEUS_API_KEY,
        "client_secret": AMADEUS_API_SECRET,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.RequestException as e:
        print(f"Token request failed: {e}")
        return None


def get_flight_pricing(
    origin: str,
    destination: str,
    departure_date: str,
    max: int,
    adults: int,
    children: int,
) -> dict:
    """
    Get flight pricing from Amadeus API.
    originLocationCode: str: IATA code of the origin airport (e.g., 'JFK').
    destinationLocationCode: str: IATA code of the destination airport (e.g., 'LAX').
    departure_date: str: Date of departure in 'YYYY-MM-DD' format.
    max: int: number of results to return.
    adults: int: Number of adults traveling.
    children: int: Number of children traveling.
    """
    token = get_bearer_token()
    if not token:
        return {"error": "Failed to obtain bearer token"}

    url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={origin}&destinationLocationCode={destination}&departureDate={departure_date}&adults={adults}&children={children}&max={max}"

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as http_err:
        return {"error": f"HTTP error: {http_err}", "status_code": response.status_code}
    except requests.RequestException as req_err:
        return {"error": f"Request error: {req_err}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}
