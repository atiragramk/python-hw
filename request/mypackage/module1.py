import requests

BASE_GIFHY_URL = 'https://api.giphy.com/v1/gifs/'

API_KEY = 'URUUMcTVhjNpobK3ylLNDBzRw2J8uGkQ'


def search_gifs():
    try:
        query = input('Enter a search word >>> ')
        limit = int(input('How many gifs do you need? >>> '))
        response = requests.get(
            f'{BASE_GIFHY_URL}search?api_key={API_KEY}&q={query}&limit={limit}&offset=0&rating=g&lang=en&bundle=messaging_non_clips')
        if response.status_code != 200:
            response.raise_for_status()
        data = response.json()
        result_list = []
        for el in data['data']:
            url = el['embed_url']
            print(url)
            result_list.append(url)
        return result_list
    except ValueError as e:
        print(e)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
