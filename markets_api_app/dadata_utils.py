import requests
from math import sin, cos, sqrt, atan2, radians

from markets_api.settings import DADATA_API_KEY, DADATA_API_SECRET
from .models import Market


headers = {'Content-Type': 'application/json',
           'Authorization': 'Token %s' % DADATA_API_KEY,
           'X-Secret': '%s' % DADATA_API_SECRET,
           }
url = "https://cleaner.dadata.ru/api/v1/clean/address"

session = requests.Session()
session.headers.update(headers)


def get_dadata_clean_address(data: bytes) -> requests.Response:
    return session.post(url=url, data=data)


def get_lat_lon(source: dict) -> [dict, None]:
    try:
        return {'latitude': source['geo_lat'], 'longitude': source['geo_lon']}
    except KeyError:
        return None


def get_3km_market(latitude: float, longitude: float):
    fixed_price = 249.99
    fixed_dist = 3  # km
    market_price_list = []
    for market in Market.objects.all():
        diff_km = calculate_distance(db_lat=market.latitude, db_lon=market.longitude,
                                     user_lat=latitude, user_lon=longitude)
        if fixed_dist >= diff_km:
            market_price_list.append({'market': market.market_name, 'price': fixed_price})
    return market_price_list


def calculate_distance(db_lat: float, db_lon: float, user_lat: float, user_lon: float) -> float:
    # TODO: Currently calculates straight line between 2 points on map
    R = 6373.0  # approximate radius of earth in km

    lat1 = radians(db_lat)
    lon1 = radians(db_lon)
    lat2 = radians(user_lat)
    lon2 = radians(user_lon)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance
