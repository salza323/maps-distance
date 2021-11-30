import json

import geopy.distance
import requests
from django.http import HttpResponse
from django.shortcuts import render



# from mapsapp.models import InputLocation
# from mapsapp.models import GeoLocation
from pyapi.pyapi import settings


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
    r = result.json()
    # todo handle result status 'ZERO_RESULTS' || 'OK'
    # Will store the candidates in a dictionary.
    coordinates: dict[str, float] = {
        'lat': float((r['candidates'][0]['geometry']['location']['lat'])),
        'long': float((r['candidates'][0]['geometry']['location']['lng']))
    }

    # geopy.distance requires a tuple, so changing dictionary data to tuple
    coordinates_tuple = (coordinates['lat'], coordinates['long'])

    return coordinates_tuple


def get_distance(request):
    # request body will be a python byte so need to decode from byte and then convert to json
    r = request.body
    str_json = r.decode('utf8')
    json_obj = json.loads(str_json)

    # TODO need to figure out why not working with address
    # Get coordinates with get_coords funnction that was previously built out
    origin_coords = get_coords(json_obj.get('origin_location'))
    destination_coords = get_coords(json_obj.get('destination_location'))

    # Porvide the coordinates to geopy to calucalte the distance between the two coordinate points.
    distance = geopy.distance.distance(origin_coords, destination_coords).miles

    # return the distance that was calculated with geopy
    return render(distance)
