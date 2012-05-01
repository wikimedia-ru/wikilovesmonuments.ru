# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.conf import settings

from menu.models import MenuItem


class MenuAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'url', 'order',)
        }),
    )

    list_display = ['name', 'url', 'order',]
    ordering = ['order',]

admin.site.register(MenuItem, MenuAdmin)

