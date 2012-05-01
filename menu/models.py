from django.utils.translation import ugettext_lazy as _
from django.db import models


class MenuItem(models.Model):
    name = models.CharField(max_length=250, verbose_name=_("Name"))
    url = models.CharField(max_length=250, verbose_name=_("URL"))
    order = models.PositiveIntegerField(blank=True, default=0, verbose_name=_("Order"))

    def __unicode__(self):
        return self.name

