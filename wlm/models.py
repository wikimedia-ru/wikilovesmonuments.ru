# -*- encoding: utf-8 -*-
import os.path

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User

from tinymce import models as tinymce_models

class Region(models.Model):
    ''' One region of RF'''
    class Meta():
        ordering = ['order']
        verbose_name = _("Region of RF")

    name = models.CharField(max_length = 200)
    district = models.IntegerField(verbose_name=_("Federal district of RF"))
    order = models.IntegerField()
    latitude = models.FloatField(max_length=20, blank=True, null=True, verbose_name=_("Latitude"))
    longitude = models.FloatField(max_length=20, blank=True, null=True, verbose_name=_("Longitude"))
    scale = models.IntegerField(verbose_name=_("Scale"))
    iso_code = models.IntegerField(verbose_name=_('ISO region code'))

    def __unicode__(self):
        return self.name

class City(models.Model):
    '''One RF city'''

    class Meta():
        ordering = ['name']
        verbose_name = _("City")

    region = models.ForeignKey(Region)
    name = models.CharField(max_length=200)
    latitude = models.FloatField(max_length=20, blank=True, null=True, verbose_name=_("Latitude"))
    longitude = models.FloatField(max_length=20, blank=True, null=True, verbose_name=_("Longitude"))

    def __unicode__(self):
        return "%s, %s" % (self.region.name, self.name)

class Street(models.Model):
    '''One city street'''
    region = models.ForeignKey(Region)
    city = models.ForeignKey(City)
    name = models.CharField(max_length = 200)

    def __unicode__(self):
        return "%s, %s, %s" % (self.region.name, self.city.name, self.name)

class Monument(models.Model):
    ''' Main class for working.
    This one contains complete definition for one building. It's a heart
    for application.
    '''
    STATE_CHOICES = (
        ('R', _("Restored")),
        ('S', _("Satisfactory")),
        ('U', _("Unsatisfactory")),
        ('A', _("Accident")),
    )

    PROTECTION_CHOICES = (
        ('F', _("Federal")),
        ('R', _("Regional")),
        ('L', _("Local")),
        ('D', _("Determined")),
        ('O', _("OPOKN")),
        ('N', _("No")),
    )
    TYPE_CHOICES = (
        ('C', _("Cultural")),
        ('A', _("Architectural")),
        ('H', _("Historical")),
    )

    class Meta:
        permissions = (
            ('can_moderate', 'Can verify and change monument data'),
        )

    #minimal required fields
    # Geospatial
    region = models.ForeignKey(Region, verbose_name = _("Region of RF"))
    city = models.ForeignKey(City, verbose_name = _("City"), blank=True, null=True)
    street = models.ForeignKey(Street, verbose_name = _("Street"), blank = True, null = True)
    coord_lon = models.FloatField(max_length=20, blank=True, null=True, verbose_name=_("Longitude"))
    coord_lat = models.FloatField(max_length=20, blank=True, null=True, verbose_name=_("Latitude"))

    #Name and address
    name = models.CharField(max_length=250, blank=True, verbose_name=_("Name"))
    name_alt = models.CharField(max_length=250, blank=True, verbose_name=_("Alternative name"))
    address = models.CharField(max_length=250, blank=True, verbose_name=_("Address"))

    #Is this building a part of complex?
    complex_root = models.ForeignKey('self', blank=True, null = True, verbose_name = _("Belong to complex"))
    complex = models.BooleanField(default = False, verbose_name = _("Complex"))
    #Additional info, may be helpful during administration...
    extra_info = tinymce_models.HTMLField(blank=True, verbose_name=_("Additional"))
    state = models.CharField(max_length=1, blank=True, choices=STATE_CHOICES, verbose_name=_("State"))
    protection = models.CharField(max_length=1, blank=True, choices=PROTECTION_CHOICES, verbose_name=_("Protection class"))
    type = models.CharField(max_length = 1, choices = TYPE_CHOICES, verbose_name = _("Type class"))

    #External link to Wiki
    ruwiki = models.CharField(max_length=250, blank=True, verbose_name=_("Wikipedia article"))
    #External link to kulturnoe-nasledie.ru
    kult_id = models.BigIntegerField(blank=True, null=True, verbose_name=_("ID Kulturnoe Nasledie"))

    #Mark this true mean "We check all data"
    verified = models.BooleanField(default = False, verbose_name = _("Verified"))
    #End of minimal required fields

    def __unicode__(self):
        return "%s, %s" % (self.name, self.address)

    def show_name(self):
        return self.name or "Неизвестно"

    def show_wiki(self):
        return self.ruwiki

class MonumentPhoto(models.Model):
    def make_upload_folder(instance, filename):
        dir_name, image_name = os.path.split(filename)
        path = u"%d/%s" % (instance.house.pk, image_name)
        return path

    monument = models.ForeignKey('Monument', verbose_name=_("Monument"))
    name = models.CharField(max_length=250, blank=True, verbose_name=_("Name"))
    commons_id = models.BigIntegerField(verbose_name=_("Image page ID"))
    author = models.CharField(max_length=250, blank=True, verbose_name=_("Author"))
    datetime = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name=_("Date & time"))
    contest_year = models.IntegerField(verbose_name=_("Federal district of RF"))
    folder = models.CharField(max_length=255, verbose_name=_('Commons folder'))
    width = models.IntegerField(verbose_name=_("File width"))
    height = models.IntegerField(verbose_name=_("File height"))
    size = models.IntegerField(verbose_name=_("File size"))
    
    def __unicode__(self):
        return self.name

class MonumentPhotoRating(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User ID"))
    photo = models.ForeignKey('MonumentPhoto', verbose_name=_("Photo"))
    vote = models.IntegerField(blank=True, null=True, verbose_name=_("Vote"))

    def __unicode__(self):
        return self.title

