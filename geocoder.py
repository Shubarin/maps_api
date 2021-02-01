import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GEOCODE_API_KEY')
START_LL = os.getenv('START_LL')
SCALE = int(os.getenv('SCALE'))
LAYER = os.getenv('LAYER')


def get_static_map(ll, z, l, points):
    url = 'http://static-maps.yandex.ru/1.x/'
    x, y = map(float, ll.split(','))
    x_left = x - (z / SCALE)
    x_right = x + (z / SCALE)
    y_bottom = y - (z / SCALE)
    y_top = y + (z / SCALE)
    arg1 = ','.join([str(x_left), str(y_bottom)])
    arg2 = ','.join([str(x_right), str(y_top)])
    params = {
        'bbox': arg1 + '~' + arg2,
        'l': l,
    }
    if points:
        params['pt'] = '~'.join(points)
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
