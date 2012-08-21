# -*- coding: utf-8 -*-


from django.contrib.gis.geoip import GeoIP
import settings

def get_region(ip):
    g = GeoIP()
    return g.city(ip)['region']
