# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.conf import settings

from menu.models import MenuItem


class MenuAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'url',)
        }),
    )

    list_display = ['name', 'url',]

admin.site.register(MenuItem, MenuAdmin)

