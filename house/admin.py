# -*- coding: utf-8 -*-

import urllib, json

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.conf import settings

from house.models import Street, House, HousePhoto, HouseEvent


class StreetAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'full_name', 'type',)
        }),
    )

    list_display = ['name', 'full_name', 'type',]


class HousePhotoInline(admin.TabularInline):
    model = HousePhoto


class HouseEventInline(admin.TabularInline):
    model = HouseEvent


class HouseAdmin(admin.ModelAdmin):
    fieldsets = (
        (_("Main info"), {
            'fields': ('name', 'name_alt', 'material', 'pasport',)
        }),
        (_("Location"), {
            'fields': ('street', 'number', 'coord_lon', 'coord_lat', 'pasport_address',)
        }),
        (_("External sources"), {
            'fields': ('kult_id', 'kult_checked', 'kult_problems', 'gudea_checked', 'ruwiki',)
        }),
        (_("Safety"), {
            'fields': ('safety', 'state', 'protection',)
        }),
        (_("Safety from pasport"), {
            'fields': ('pasport_safety', 'pasport_state', 'pasport_protection',)
        }),
        (_("Ownership"), {
            'fields': ('usage', 'ownership', 'land_ownership', 'owner', 'obligation', 'lease', 'tenant',)
        }),
        (_("Additional"), {
            'fields': ('chronology', 'documents', 'monitoring', 'extra_info',)
        }),
        (_("Belong to complex"), {
            'fields': ('complex', 'complex_name', 'complex_root', 'complex_kult_id',)
        }),
    )
    inlines = (HousePhotoInline, HouseEventInline,)

    def addr(obj):
        return ("%s, %s" % (obj.street.name, obj.number))
    addr.short_description = _("Address")
    addr.admin_order_field = 'street__name'

    def map_pin(obj):
        if obj.coord_x is None:
            return '';
        out = ("<a target='_blank' href='http://maps.yandex.ru/?text=%s,+%s&ll=%s,%s&z=15&l=map'>" % \
            (obj.street.full_name, obj.number, obj.coord_x, obj.coord_y)) + \
            "<img src='/static/admin/img/ext/icon-map-pin.png' /></a>"
        return out
    map_pin.short_description = _("Map")
    map_pin.allow_tags = True
    map_pin.admin_order_field = 'coord_x'

    def kult_url(obj):
        if obj.kult_id == 0:
            return '';
        icon = 'no'
        if obj.kult_checked:
            icon = 'yes'
        out = ("<img src='/static/admin/img/admin/icon-%s.gif' alt='%s' /> " % \
            (icon, obj.kult_checked)) + \
            ("<a href='http://kulturnoe-nasledie.ru/monuments.php?id=%s'>%s</a>" % \
            (obj.kult_id, obj.kult_id))
        return out
    kult_url.short_description = _("ID Kulturnoe Nasledie")
    kult_url.allow_tags = True
    kult_url.admin_order_field = 'kult_id'

    list_display = [addr, 'name', map_pin, kult_url, 'safety', 'state',
        'usage', 'protection', 'ownership', 'pasport', 'obligation',
        'material', 'owner', 'tenant', 'extra_info',]
    ordering = ['street__name', 'number',]

    list_filter = ['safety', 'state', 'usage', 'protection', 'material',]
    search_fields = ['kult_id',]

admin.site.register(Street, StreetAdmin)
admin.site.register(House, HouseAdmin)

