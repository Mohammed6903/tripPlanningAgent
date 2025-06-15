import requests


def get_currency_rate(from_currency: str, to_currency: str) -> dict:
    url = f"https://api.frankfurter.app/latest?from={from_currency}&to={to_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rate = data["rates"][to_currency]
        return {
            "status": "success",
            "rate": rate,
            "info": f"1 {from_currency} = {rate} {to_currency}",
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
