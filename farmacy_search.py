import os
import sys

from business import find_business
from distance import lonlat_distance
from geocoder import get_coordinates, get_ll_span
from mapapi_PG import show_map
import requests
import pygame
import json

API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


def main():
    toponym_to_find = input('Что будем искать?\n')

    # Формируем параметры запроса по основнуму адресу
    ll, spn = get_ll_span(toponym_to_find)
    lat, lon = map(float, ll.split(","))

    # Получаем координаты ближайшей аптеки.
    organization = find_business(ll, spn, "аптека")
    point = organization["geometry"]["coordinates"]
    org_lat = float(point[0])
    org_lon = float(point[1])

    # Сниппет
    # Название организации.
    name = organization["properties"]["CompanyMetaData"]["name"]
    # Адрес организации.
    address = organization["properties"]["CompanyMetaData"]["address"]
    # Время работы
    time = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
    # Расстояние 
    distance = round(lonlat_distance((lon, lat), (org_lon, org_lat)))

    snippet = [
        f"Аптека: {name}",
        f"Адрес: {address}",
        f"Время работы: {time}",
        f"Расстояние: {distance} м."
    ]

    # print(snippet," Формируем параметры для карты")
    map_param = {
        "ll": ll,
        "spn": ','.join([str(abs(lat - org_lat) * 2), str(abs(lon - org_lon) * 2)]),
        # Масштабирование с учетом растояний
        "l": "map",
        "pt": f"{ll}~{org_lat},{org_lon},pm2dgl"
    }
    # print(map_param)

    show_map(params=map_param, text=snippet)


if __name__ == "__main__":
    main()
