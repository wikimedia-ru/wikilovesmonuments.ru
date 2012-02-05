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
            'fields': ('street', 'number', 'name', 'kult_id', 'kult_checked',
            'safety', 'state', 'usage', 'protection', 'ownership', 'pasport',
            'obligation', 'material', 'owner', 'tenant', 'extra_info',)
        }),
    )
    inlines = (HousePhotoInline, HouseEventInline,)

    def addr(obj):
        return ("%s, %s" % (obj.street.name, obj.number))
    addr.short_description = _("Address")

    def kult_url(obj):
        if obj.kult_id == 0:
            return '';
        icon = 'no'
        if obj.kult_checked:
            icon = 'yes'
        out = ("<img src='/static/admin/img/admin/icon-%s.gif' alt='%s' /> " % (icon, obj.kult_checked))
        out += ("<a href='http://kulturnoe-nasledie.ru/monuments.php?id=%s'>%s</a>" % (obj.kult_id, obj.kult_id))
        return out
    kult_url.short_description = _("ID Kulturnoe Nasledie")
    kult_url.allow_tags = True

    list_display = [addr, 'name', kult_url, 'safety', 'state',
        'usage', 'protection', 'ownership', 'pasport', 'obligation',
        'material', 'owner', 'tenant', 'extra_info',]
    ordering = ['street__name', 'number',]

    list_filter = ['safety', 'state', 'usage', 'protection', 'material',]
    search_fields = ['kult_id',]


admin.site.register(Street, StreetAdmin)
admin.site.register(House, HouseAdmin)

