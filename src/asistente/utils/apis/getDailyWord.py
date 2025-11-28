import requests

def get_daily_word():
    """Obtener la palabra del día"""
    try:
        url = "https://rae-api.com/api/daily"
        headers = {"Accept": "application/json"}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
