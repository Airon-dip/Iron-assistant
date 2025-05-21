import webbrowser
import requests
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import geocoder

def loc(place):
    webbrowser.open("http://www.google.com/maps/place/" + place)
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.geocode(place, addressdetails=True)

    if location is None:
        return None, None, None  # Если местоположение не найдено

    target_latlng = (location.latitude, location.longitude)
    address = location.raw['address']
    target_loc = {
        'город': address.get('city', '') or address.get('town', '') or address.get('village', ''),
        'регион': address.get('state', ''),
        'страна': address.get('country', '')
    }

    current_loc = geocoder.ip('me')
    current_latlng = current_loc.latlng

    if current_latlng is None:
        return None, None, None  # Если текущее местоположение не найдено

    distance = great_circle(current_latlng, target_latlng).kilometers
    distance = round(distance, 2)

    return current_loc, target_loc, distance

def my_location():
    ip_add = requests.get('https://api.ipify.org').text
    url = 'https://get.geojs.io/v1/ip/geo/' + ip_add + '.json'
    geo_requests = requests.get(url)
    geo_data = geo_requests.json()

    city = geo_data.get('city', '')
    state = geo_data.get('region', '')
    country = geo_data.get('country', '')

    return city, state, country