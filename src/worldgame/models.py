# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class Country(models.Model):
    "Country model."
    name = models.CharField(_('name'), max_length=99,
                            unique=True, db_index=True)
    geom = models.MultiPolygonField(_('geometry'), dim=2, srid=900913)
    population = models.IntegerField(_('population'), default=0)

    objects = models.GeoManager()

    class Meta:
        db_table = 'country'
        ordering = ('-population',)
        verbose_name = _('country')
        verbose_name_plural = _('countries')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('show_country', (self.id,))


class Highscore(models.Model):
    "Scores model."
    name = models.CharField(_('name'), max_length=30)
    score = models.IntegerField(_('score'), default=0)

    class Meta:
        db_table = 'highscore'
        ordering = ('-score',)
        verbose_name = _('high score')
        verbose_name_plural = _('high scores')

    def __unicode__(self):
        return self.name
