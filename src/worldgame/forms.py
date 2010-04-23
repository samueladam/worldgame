# -*- coding: utf-8 -*-
from django.contrib.gis import admin
from django import forms

from .models import Country

# create a geoadmin instance
geoadmin = admin.GeoModelAdmin(Country, admin.site)
geoadmin.num_zoom = 4
geoadmin.modifiable = False
geoadmin.layerswitcher = False
geoadmin.mouse_position = False
geoadmin.scale_text = False

# get the Open Layers widget for the geom field
field = Country._meta.get_field('geom')
widget = geoadmin.get_map_widget(field)


class CountryForm(forms.ModelForm):
    "This form is a hack to display an OpenLayers map."
    geom = forms.CharField(widget=widget)

    class Meta:
        model = Country
        fields = ('name', 'geom',)

    class Media:
        js = (geoadmin.openlayers_url,)
