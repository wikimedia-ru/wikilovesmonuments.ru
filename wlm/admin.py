# -*- coding: utf-8 -*-

import urllib, json

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.conf import settings

from models import Region, City, Street, Monument


class StreetAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', )
        }),
    )

    list_display = ['name','city', 'region' ]
    list_filter = ['city']

class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','order']

class MonumentAdmin(admin.ModelAdmin):
    fieldsets = (
        (_("Main info"), {
            'fields': ('name', 'name_alt', )
        }),
        (_("Location"), {
            'fields': ('region', 'city', 'street', 'address','coord_lon', 'coord_lat',)# 'pasport_address',)
        }),
        (_("Complex"), {
            'fields': ('complex',)
        }),
        (_("Safety"), {
            'fields': ('state', 'protection', 'type',)
        }),
        (_("Extra"), {
            'fields': ('extra_info', 'verified', 'kult_id', 'ruwiki',)
        })

    )
    list_filter = ['complex', 'region']
    list_display = ['show_name', 'region', 'city', 'show_wiki', 'verified',]

admin.site.register(Street, StreetAdmin)
admin.site.register(Monument, MonumentAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(City)
