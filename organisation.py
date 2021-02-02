import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('ORGANISATION_API_KEY')

def find_organisation(ll):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    search_params = {
        "apikey": API_KEY,
        "lang": "ru_RU",
        "text": "организации",
        "spn": "0.00009,0.00009",
        "ll": ll,
        "type": "biz"
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        pass
    json_response = response.json()
    try:
        organization = json_response["features"][0]
        org_name = organization["properties"]["CompanyMetaData"]["name"]
        org_address = organization["properties"]["CompanyMetaData"]["address"]
        org_allowed = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
        coords = organization["geometry"]["coordinates"]

        info = '\n'.join([org_name, org_address, org_allowed])
        return info
    except Exception:
        return ''