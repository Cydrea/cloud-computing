import requests
import json

''' official website  https://www.qweather.com '''
'''      dev website  https://dev.qweather.com'''

# API authentication key
KEY = '6d76a5bd96da4eada10fbf19c7077fbb'
mykey = '&key=' + KEY

url_api_weather = 'https://devapi.qweather.com/v7/weather/'
url_api_geo = 'https://geoapi.qweather.com/v2/city/'


def get(city_id):
    url = url_api_weather + 'now' + '?location=' + city_id + mykey + '&lang=en'
    return requests.get(url).json()


def get_city(city_kw):
    url_v2 = url_api_geo + 'lookup?location=' + city_kw + mykey + '&lang=en'
    city = requests.get(url_v2).json()['location'][0]

    city_id = city['id']
    district_name = city['name']
    city_name = city['adm2']
    province_name = city['adm1']
    country_name = city['country']

    return city_id, district_name, city_name, province_name, country_name


if __name__ == '__main__':
    if KEY == '':
        print('No Key! Get it first!')


def print_weather(x):
    city_input = x
    city_idname = get_city(city_input)
    city_id = city_idname[0]
    get_now = get(city_id)

    if city_idname[2] == city_idname[1]:
        a = [city_idname[3], str(city_idname[2])]
    else:
        a = [city_idname[3], str(city_idname[2]), str(city_idname[1]) + ' District']
    b = ['Now Weather:', get_now['now']['text'], '; Now temp:', get_now['now']['temp'],
         '°C', '; feels like:', get_now['now']['feelsLike'], '°C']

    c = str(a) + str(b)

    return c
