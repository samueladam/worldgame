# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


COLORS = (
    (0, _('black')),
    (1, _('white')),
)

class Country(models.Model):
    "Explain what Example is for."
    name = models.CharField(_('name'), max_length=50)
    details = models.TextField(_('details'), blank=True, null=True)
    user = models.ForeignKey(User, related_name="examples")
    timestamp = models.DateTimeField(default=datetime.now)
    counter = models.PositiveIntegerField(_('counter'), default=0)
    color = models.PositiveSmallIntegerField(_('color'), choices=COLORS,
                                     default=COLORS[0][0])

    class Meta:
        db_table = 'countrys'
        ordering = ('-timestamp',)
        verbose_name = _('country')
        verbose_name_plural = _('countrys')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Country, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('show_country', (self.id,))


