import requests
import os
import json

SERPER_API_KEY = os.getenv("SERPER_API_KEY")


def serper_search(query: str, type: str = "search") -> dict:
    """
    searches the Serper API for a given query and type.
    query: str: The search query to be sent to the Serper API.
    type: str: The type of search to perform (e.g., "search", "places").

    """
    url = "https://google.serper.dev/{type}".format(type=type)

    payload = json.dumps({"q": query})

    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=payload)

    return response.json()
