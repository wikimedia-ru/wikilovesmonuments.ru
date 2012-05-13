import os.path

from django.utils.translation import ugettext_lazy as _
from django.db import models

from tinymce import models as tinymce_models
from yafotki.fields import YFField


class Region(models.Model):
    name = models.CharField(max_length=250, verbose_name=_("Name"))
    coord = models.CharField(max_length=20, verbose_name=_("Coordinates"))

    def __unicode__(self):
        return self.name


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
    description = tinymce_models.HTMLField(blank=True, verbose_name=_("Description"))

    class Meta:
        ordering = ['name',]

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
        ('U', _("Unsatisfactory")),
        ('A', _("Accident")),
    )
    
    USAGE_CHOICES = (
        ('H', _("Dwelling house")),
        ('O', _("Office building")),
    )
    
    PROTECTION_CHOICES = (
        ('F', _("Federal")),
        ('R', _("Regional")),
        ('L', _("Local")),
        ('D', _("Determined")),
        ('O', _("OPOKN")),
        ('N', _("No")),
    )
    
    OWNERSHIP_CHOICES = (
        ('F', _("Federal")),
        ('R', _("Regional")),
        ('M', _("Municipal")),
    )
    
    MATERIAL_CHOICES = (
        ('W', _("Wooden")),
        ('S', _("Stone")),
    )
    
    LEASE_CHOICES = (
        ('L', _("Lease")),
        ('R', _("Rent")),
    )
    
    kult_id = models.PositiveIntegerField(blank=True, null=True, verbose_name=_("ID Kulturnoe Nasledie"))
    ruwiki = models.CharField(max_length=250, blank=True, verbose_name=_("Wikipedia article"))

    name = models.CharField(max_length=250, blank=True, verbose_name=_("Name"))
    name_alt = models.CharField(max_length=250, blank=True, verbose_name=_("Alternative name"))
    material = models.CharField(max_length=1, blank=True, choices=MATERIAL_CHOICES, verbose_name=_("Material"))
    pasport = models.BooleanField(blank=True, verbose_name=_("Pasport status"))

    street = models.ForeignKey('Street', verbose_name=_("Street"))
    number = models.CharField(max_length=20, verbose_name=_("Number"))
    coord_lon = models.FloatField(max_length=20, blank=True, null=True, verbose_name=_("Longitude"))
    coord_lat = models.FloatField(max_length=20, blank=True, null=True, verbose_name=_("Latitude"))
    pasport_address = models.CharField(max_length=250, blank=True, verbose_name=_("Address from pasport"))

    safety = models.CharField(max_length=1, blank=True, choices=SAFETY_CHOICES, verbose_name=_("Safety"))
    state = models.CharField(max_length=1, blank=True, choices=STATE_CHOICES, verbose_name=_("State"))
    protection = models.CharField(max_length=1, blank=True, choices=PROTECTION_CHOICES, verbose_name=_("Protection class"))

    pasport_safety = models.CharField(max_length=1, blank=True, choices=SAFETY_CHOICES, verbose_name=_("Safety from pasport"))
    pasport_state = models.CharField(max_length=1, blank=True, choices=STATE_CHOICES, verbose_name=_("State from pasport"))
    pasport_protection = models.CharField(max_length=1, blank=True, choices=PROTECTION_CHOICES, verbose_name=_("Protection class"))

    usage = models.CharField(max_length=1, blank=True, choices=USAGE_CHOICES, verbose_name=_("Usage"))
    ownership = models.CharField(max_length=1, blank=True, choices=OWNERSHIP_CHOICES, verbose_name=_("Ownership"))
    land_ownership = models.CharField(max_length=1, blank=True, choices=OWNERSHIP_CHOICES, verbose_name=_("Land ownership"))
    owner = models.CharField(max_length=250, blank=True, verbose_name=_("Owner"))
    obligation = models.DateField(blank=True, null=True, verbose_name=_("Obligation date"))
    lease = models.CharField(max_length=1, blank=True, choices=LEASE_CHOICES, verbose_name=_("Lease/Rent"))
    tenant = models.CharField(max_length=250, blank=True, verbose_name=_("Tenant"))

    chronology = tinymce_models.HTMLField(blank=True, verbose_name=_("Cronology")) # temporary
    documents = tinymce_models.HTMLField(blank=True, verbose_name=_("Documents")) # temporary
    monitoring = tinymce_models.HTMLField(blank=True, verbose_name=_("Monitoring")) # temporary

    complex = models.BooleanField(blank=True, verbose_name=_("Complex"))
    complex_root = models.ForeignKey('House', blank=True, null=True, verbose_name=_("Belong to complex"))
    complex_name = models.CharField(max_length=250, blank=True, verbose_name=_("Name")) # temporary
    complex_kult_id = models.PositiveIntegerField(blank=True, null=True, verbose_name=_("ID Kulturnoe Nasledie")) # temporary

    extra_info = tinymce_models.HTMLField(blank=True, verbose_name=_("Additional"))

    kult_checked = models.BooleanField(default=False, verbose_name=_("ID Kulturnoe Nasledie checked")) # temporary
    kult_problems = models.CharField(max_length=20, blank=True, verbose_name=_("Kulturnoe Nasledie problems")) # temporary
    gudea_checked = models.BooleanField(default=False, verbose_name=_("Gudea base checked")) # temporary

    def __unicode__(self):
        return self.street.name + ', ' + self.number


class HousePhoto(models.Model):
    def make_upload_folder(instance, filename):
        dir_name, image_name = os.path.split(filename)
        path = u"%d/%s" % (instance.house.pk, image_name)
        return path

    house = models.ForeignKey('House', verbose_name=_("House"))
    file = YFField(upload_to=make_upload_folder)
    title = models.CharField(max_length=250, blank=True, verbose_name=_("Title"))
    author = models.CharField(max_length=250, blank=True, verbose_name=_("Author"))

    def __unicode__(self):
        return self.title


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
        return self.date + ' - ' + self.text

