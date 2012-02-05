from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from house.models import Street, House, HousePhoto, HouseEvent


class StreetAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'full_name', 'type',)
        }),
    )

    list_display = ['name', 'full_name', 'type',]
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

    list_display = ['street', 'number', 'name', 'kult_id', 'safety', 'state',
        'usage', 'protection', 'ownership', 'pasport', 'obligation',
        'material', 'owner', 'tenant', 'extra_info',]
    ordering = ['street', 'number',]

    list_filter = ['safety', 'state', 'usage', 'protection', 'material',]
    search_fields = ['kult_id',]


admin.site.register(Street, StreetAdmin)
admin.site.register(House, HouseAdmin)

