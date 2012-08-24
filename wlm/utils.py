# -*- coding: utf-8 -*-


from django.contrib.gis.geoip import GeoIP
import settings


def get_region(ip):
    g = GeoIP()
    try:
        code = g.city(ip)['region']
    except:
        code = "47"
    if code == "48": 
        code = "47"  #Moscow
    elif code == "66":
        code = "42"  #Spb

    return code
