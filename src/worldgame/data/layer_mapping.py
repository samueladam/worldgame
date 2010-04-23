#!/home/sam/code/worldgame/parts/pip/bin/python

import sys
sys.path[0:0] = [
  '/home/sam/code/worldgame/parts/pip/lib/python2.5/site-packages',
  '/home/sam/code/worldgame/src',
  ]


import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'worldgame.test_settings'


from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.geos import MultiPolygon

from worldgame.models import Country

country_mapping = {
    'name': 'NAME',
    'geom': 'MULTIPOLYGON',
    'population' : 'POP2005',
}

lm = LayerMapping(Country, # django model
                  'TM_WORLD_BORDERS-0.3.shp', # source file
                  country_mapping, # field to field mapping
                  encoding='iso-8859-1')


# Antartica (id 145) doesn't convert to srid 900913, skip it
lm.save(fid_range=(1, 144), verbose=True)
lm.save(fid_range=(146, 246), verbose=True)


# Simplify the shapes
for country in Country.objects.all():
    geom = country.geom.simplify(tolerance=1000, preserve_topology=True)
    if geom.num_geom == 1:
        geom = MultiPolygon(geom)
    country.geom = geom
    country.save()
