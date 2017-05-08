#!/usr/bin/env python

# coding: utf-8

import requests
import json
from urllib.parse import urlencode
from haversine import haversine
import sys
from tabulate import tabulate


API_URL = "https://maps.googleapis.com/maps/api/geocode/json"
API_VELOV_URL = "https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json"


def getPostion(address):
    param = { 'address':address}
    res = json.loads(requests.get("{}?{}".format(API_URL,urlencode(param))).text)
    location = res['results'][0]["geometry"]["location"]
    return float(location['lat']),float(location['lng'])


def get_stations():
    return json.loads(requests.get(API_VELOV_URL).text)["values"]


def add_distance(stations, pos):
    for s in stations:
        pos_station = (float(s["lat"]),float(s["lng"]))
        s["distance"] = haversine(pos, pos_station)


def sort_stations(stations):
    return sorted(stations, key=lambda x: x["distance"])


def get_closest_stations(address):
    stations = get_stations()
    add_distance(stations, getPostion(address))
    return sort_stations(stations)[:10]


def main():
    address = sys.argv[1]
    stations = get_closest_stations(address)
    res = []
    for s in stations:
        res.append([s["address"],s["available_bikes"],s["available_bike_stands"]])
        #print("{} - {} - {}".format(s["address"],s["available_bikes"],s["available_bike_stands"]))
    print(tabulate(res, headers=("Adresse","Vélos libres","Places restantes")))

if __name__=="__main__":
	main()
