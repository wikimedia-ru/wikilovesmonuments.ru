import os.path

from django.utils.translation import ugettext_lazy as _
from django.db import models



class Street(models.Model):
    STREET_CHOICES = (
        ('S', _("Street")),
        ('L', _("Lane")),
        ('H', _("Highway")),
        ('Q', _("Square")),
        ('E', _("Embankment")),
        ('P', _("Passage")),
        ('A', _("Avenue")),
        ('B', _("Blind alley")),
    )

    name = models.CharField(max_length=250, verbose_name=_("Name"))
    full_name = models.CharField(blank=True, max_length=250, verbose_name=_("Full name"))
    type = models.CharField(max_length=1, blank=True, choices=STREET_CHOICES, default='S', verbose_name=_("Type"))

    def __unicode__(self):
        return self.name


class House(models.Model):
    SAFETY_CHOICES = (
        ('S', _("Saved")),
        ('M', _("Modern replica")),
        ('R', _("Ruins")),
        ('L', _("Losed")),
    )
    
    STATE_CHOICES = (
        ('R', _("Restored")),
        ('S', _("Satisfactory")),
        ('A', _("Accident")),
    )
    
    USAGE_CHOICES = (
        ('H', _("Dwelling house")),
        ('O', _("Office building")),
    )
    
    PROTECTION_CHOICES = (
        ('F', _("Federal")),
        ('R', _("Regional")),
        ('O', _("OPOKN")),
        ('D', _("Determined")),
        ('N', _("No")),
    )
    
    MATERIAL_CHOICES = (
        ('W', _("Wood")),
        ('S', _("Stone")),
    )
    
    kult_id = models.PositiveIntegerField(blank=True, null=True, verbose_name=_("ID Kulturnoe Nasledie"))
    name = models.CharField(max_length=250, blank=True, verbose_name=_("Name"))
    street = models.ForeignKey('Street', verbose_name=_("Street"))
    number = models.CharField(max_length=20, verbose_name=_("Number"))
    coord_x = models.FloatField(max_length=20, blank=True, null=True, verbose_name=_("Coord X"))
    coord_y = models.FloatField(max_length=20, blank=True, null=True, verbose_name=_("Coord Y"))
    safety = models.CharField(max_length=1, blank=True, choices=SAFETY_CHOICES, verbose_name=_("Safety"))
    state = models.CharField(max_length=1, blank=True, choices=STATE_CHOICES, verbose_name=_("State"))
    usage = models.CharField(max_length=1, blank=True, choices=USAGE_CHOICES, verbose_name=_("Usage"))
    protection = models.CharField(max_length=1, blank=True, choices=USAGE_CHOICES, verbose_name=_("Protection class"))
    ownership = models.CharField(max_length=250, blank=True, verbose_name=_("Ownership"))
    pasport = models.BooleanField(blank=True, verbose_name=_("Pasport status"))
    obligation = models.CharField(max_length=250, blank=True, verbose_name=_("Obligation"))
    material = models.CharField(max_length=1, blank=True, choices=USAGE_CHOICES, verbose_name=_("Material"))
    owner = models.CharField(max_length=250, blank=True, verbose_name=_("Owner"))
    tenant = models.CharField(max_length=250, blank=True, verbose_name=_("Tenant"))
    extra_info = models.TextField(blank=True, verbose_name=_("Additional"))

    def __unicode__(self):
        return self.street.name + ', ' + self.number


class HousePhoto(models.Model):
    def make_upload_path(instance, filename):
        path = u"%u%s" % (instance.house.pk, os.path.splitext(filename)[1])
        i = 0
        while (os.path.isfile(path)):
            path = u"%u_%u%s" % (instance.page.code1, i, os.path.splitext(filename)[1])
        return path

    house = models.ForeignKey('House', verbose_name=_("House"))
    file = models.FileField(upload_to=make_upload_path, blank=True, null=True, verbose_name=_("File"))
    title = models.CharField(max_length=250, blank=True, verbose_name=_("Title"))

    def __unicode__(self):
        return '[' + self.house + ']' + self.title


class HouseEvent(models.Model):
    TYPE_CHOICES = (
        ('P', _("Projected")),
        ('B', _("Builded")),
        ('R', _("Restored")),
        ('D', _("Demolished")),
    )
    
    house = models.ForeignKey('House', verbose_name=_("House"))
    date = models.CharField(max_length=250, blank=True, verbose_name=_("Date"))
    type = models.CharField(max_length=1, blank=True, choices=TYPE_CHOICES, verbose_name=_("Event type"))
    comment = models.CharField(max_length=250, blank=True, verbose_name=_("Comment"))

    def __unicode__(self):
        return '[' + self.house + ']' + ' ' + self.date + ' - ' + self.text

