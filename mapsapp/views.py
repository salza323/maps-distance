from typing import Dict

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse

import json
import requests
import geopy.distance


# from mapsapp.models import InputLocation
# from mapsapp.models import GeoLocation


def index(request):
    response = json.dumps([{}])
    return HttpResponse(response, content_type='text/json')


'''
sample request
request = {
    'origin_location': 'Disneyland',
    'destination_location': '3757WestwoodBlvdLosAngeles,CA90034',
}
'''

# TODO - get coords
def get_coords(location):
    poi = location

    result = requests.get(
        'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?',
        params={
            'input': poi,
            'inputtype': 'textquery',
            'fields': 'formatted_address,name,geometry',
            'key': settings.GOOGLE_API_KEY
        })
    # TODO will need to know what the result looks like
    print('apikey', settings.GOOGLE_API_KEY)
    print('result', result.json())
    r = result.json()
    # todo handle result status 'ZERO_RESULTS' || 'OK'
    coordinates: dict[str, float] = {
        'lat': float((r['candidates'][0]['geometry']['location']['lat'])),
        'long': float((r['candidates'][0]['geometry']['location']['lng']))
    }

    coordinates_tuple = (coordinates['lat'], coordinates['long'])

    return coordinates_tuple


# TODO - get distance between two coords set
def get_distance(request):
    r = request.body
    str_json = r.decode('utf8')
    json_obj = json.loads(str_json)
    print('origin', json_obj.get('origin_location'))
    print('destination', json_obj.get('destination_location'))

    origin_coords = get_coords(json_obj.get('origin_location'))
    print('origin_coords', origin_coords)
    # TODO need to figure out why not working with address
    destination_coords = get_coords(json_obj.get('destination_location'))
    print('destination_coords', destination_coords)

    distance = geopy.distance.distance(origin_coords, destination_coords).miles

    print(origin_coords)
    print(destination_coords)
    print('distance', distance)

    return distance
