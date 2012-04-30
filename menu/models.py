from django.utils.translation import ugettext_lazy as _
from django.db import models


class MenuItem(models.Model):
    name = models.CharField(max_length=250, verbose_name=_("Name"))
    url = models.CharField(max_length=250, verbose_name=_("URL"))

    def __unicode__(self):
        return self.name

