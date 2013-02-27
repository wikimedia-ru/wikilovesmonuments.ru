from django.contrib.gis.geoip import GeoIP
import re
import settings


def get_region(ip):
    default_code = '47' # Moscow
    g = GeoIP()
    try:
        ip = re.sub(r'^::ffff:', '', ip)
        city = g.city(ip)
        if city['country_code'] == 'RU':
            code = city['region']
        else:
            code = default_code
    except:
        code = default_code
    if code == '48': 
        code = '47'  # Moscow
    elif code == '66':
        code = '42'  # Spb

    return code
