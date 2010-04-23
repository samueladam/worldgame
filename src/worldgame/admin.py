from django.contrib.gis import admin

from .models import Country


class CountryAdmin(admin.OSMGeoAdmin):
    pass

admin.site.register(Country, CountryAdmin)
