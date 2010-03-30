from django.contrib import admin

from .models import Country

class CountryAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = ('name', 'timestamp')

admin.site.register(Country, CountryAdmin)
