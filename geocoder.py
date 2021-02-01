import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GEOCODE_API_KEY')
START_LL = os.getenv('START_LL')
Z = os.getenv('Z')
LAYER = os.getenv('LAYER')


def get_static_map(ll=START_LL, z=Z, l=LAYER):
    url = 'http://static-maps.yandex.ru/1.x/'
    params = {
        'll': ll,
        'l': l,
        'z': z
    }
    response = requests.get(url, params)
    if not response:
        return
    return response.content


def get_coordinate(address):
    url = 'http://geocode-maps.yandex.ru/1.x/'
    params = {
        'apikey': API_KEY,
        'geocode': address,
        'format': 'json'
    }
    response = requests.get(url=url, params=params)
    if response:
        json_response = response.json()
        toponym = \
        json_response["response"]["GeoObjectCollection"]["featureMember"][0][
            "GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        ll = ','.join(toponym_coodrinates.split())
        return ll


if __name__ == '__main__':
    pass
