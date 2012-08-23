# -*- coding: utf-8 -*-


from django.contrib.gis.geoip import GeoIP
import settings


def get_region(ip):
    g = GeoIP()
    code = g.city(ip)['region']
    if code == "48": 
        code = "47"  #Moscow
    elif code == "66":
        code = "42"  #Spb

    return code
