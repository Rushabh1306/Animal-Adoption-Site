# Helper Functions
import django.contrib.gis.geoip2


def get_geo(ip):
    g = django.contrib.gis.geoip2.GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    lat, long = g.lat_lon(ip)
    return country, city, lat, long


def get_center_coordinates(latA, longA, latB=None, longB=None):
    cord = latA, longA
    if latB:
        cord = [(latA + latB) / 2, (longA + longB) / 2]
    return cord


def getZoom(distance):
    if distance <= 100:
        return 8
    elif 100 < distance <= 5000:
        return 4
    else:
        return 2

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_five_organizations(lat,long):
    pass
