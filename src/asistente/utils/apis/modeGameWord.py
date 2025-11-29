import requests

def modeGameWord(mode):
    """Obtener la palabra del día"""
    try:
        url = f"https://rae-api.com/api/{mode}"
        headers = {"Accept": "application/json"}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
