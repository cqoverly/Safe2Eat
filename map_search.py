#! /usr/bin/env python

import urllib
import urllib2
from pprint import pprint
try:
    import simplejson as json
except ImportError:
    import json


API_KEY = 'AIzaSyCFNabJBDvXBcMzetmQU715yByGRExw1Mw'
TEXT_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
NEARBY_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'


def get_start_loc(address):
    # Takes an address and converts it to a tuple containg latitude and longitude of address.
    params = urllib.urlencode({'query': address, 'sensor': 'false', 'key': API_KEY})
    url = TEXT_URL+params
    res = urllib2.urlopen(url)
    info = json.loads(res.read())
    lat, lng = (info['results'][0]['geometry']['location']['lat'], info['results'][0]['geometry']['location']['lng'])
    return '%s,%s' % (lat, lng)


def get_list(coords, miles):
    """
    Calls Google Places API to generate list (limited to 20 by google without extra code) 
    of restaurants within the miles passed in the args. Coordinates were created by the get_start_loc(addresss)
    method. 
    """

    radius = int(round(miles * 1609.34))  # converts miles to meters, as needed by google API.
    params = urllib.urlencode({'location': coords, 'radius': radius, 'types': 'restaurant', 'sensor': 'false', 'key': API_KEY})

    search_url = NEARBY_URL + params
    # print search_url

    res = urllib2.urlopen(search_url)
    search_list = res.read()
    return json.loads(search_list)  #  return pythonized results.

def display_list(search_list):
    """
    Used for testing. Can also be used for a standalone search, not including inspection info.
    """
    count = 1

    for result in search_list['results']:
        print '<<<<<<<<<<<<<', count,' >>>>>>>>>>>>>>>'
        print "Name: ", result['name']
        try:
            print "Rating: ", result['rating']
        except KeyError:
            pass
        try:
            print "Price Level: ", result['price_level']
        except KeyError:
            pass
        print "Address: ", result['vicinity']
        print '======================================'
        print
        count += 1
    print 'END OF LIST'

def process_list(search_list):
    """
    Takes pythonized json list of restaurants and their info and places it into a list 
    of dicts, each dict holding the information for one listing. This dict will be added to 
    with inspection information.
    """
    rest_info = []  #  List to hold dicts of attributes for each restauraing in list.
    for rest in search_list['results']:  # Generate dict for each listing.
        restaurant = dict()
        restaurant['Name'] = rest['name']
        try:                 
            restaurant['Rating'] = rest['rating']    #  See if listing has attribute.
        except KeyError:           
            pass                                     #  Keep going without adding attribute.
        try:
            restaurant['Price Level'] = rest['price_level']  #  Same as above
        except KeyError:
            pass
        restaurant['Address'] = rest['vicinity']

        rest_info.append(restaurant)  # Add dict to list of restaurants.
    return rest_info


if __name__ == '__main__':
    address = '3827 Interlake Ave N 98103'
    coords = get_start_loc(address) 
    print coords
    search_list = get_list(coords, 2)
    display_list(search_list)