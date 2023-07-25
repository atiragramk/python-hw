import requests
import os

BASE_GIFHY_URL = os.environ.get('BASE_GIFHY_URL')

API_KEY = os.environ.get('API_KEY')


def search_gifs(query: str, limit: int):
    try:
        if not limit.isdigit():
            raise ValueError
        response = requests.get(
            f'{BASE_GIFHY_URL}search?api_key={API_KEY}&q={query}&limit={limit}&offset=0&rating=g&lang=en&bundle=messaging_non_clips')
        if response.status_code != 200:
            response.raise_for_status()
        data = response.json()
        result_list = []
        for el in data['data']:
            url = el['images']['original']['url']
            print(url)
            result_list.append(url)
        return result_list
    except ValueError as e:
        print(e)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
