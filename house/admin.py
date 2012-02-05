from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from house.models import Street, House, HousePhoto, HouseEvent


class StreetAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
    )

    list_display = ['name',]
    ordering = ['name',]


class HousePhotoInline(admin.TabularInline):
    model = HousePhoto


class HouseEventInline(admin.TabularInline):
    model = HouseEvent


class HouseAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('street', 'number', 'name', 'kult_id', 'safety', 'state',
            'usage', 'protection', 'ownership', 'pasport', 'obligation',
            'material', 'owner', 'tenant', 'extra_info',)
        }),
    )
    inlines = (HousePhotoInline, HouseEventInline,)

    list_display = ['street', 'number', 'name',]
    ordering = ['street', 'number',]


admin.site.register(Street, StreetAdmin)
admin.site.register(House, HouseAdmin)

