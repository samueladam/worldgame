#!/home/sam/code/worldgame/parts/pip/bin/python

import sys
sys.path[0:0] = [
  '/home/sam/code/worldgame/parts/pip/lib/python2.5/site-packages',
  '/home/sam/code/worldgame/src',
  ]


import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'worldgame.test_settings'


from django.contrib.gis.gdal.datasource import DataSource
from django.contrib.gis.gdal.geometries import MultiPolygon
from django.contrib.gis.geos import Point, Polygon
from django.contrib.gis.utils import LayerMapping

from worldgame.models import Country

# open ERSI Shapefile
ds = DataSource('TM_WORLD_BORDERS-0.3.shp')
print '* DataSource:', ds

# Shapefiles have only one layer
layer = ds[0]
print '* Layer:', layer
print '* Layer Shape:', layer.geom_type
print '* Features Shape:', layer[0].geom.geom_type
print '* Number of features:', len(layer)
print '* Layer additional fields:', layer.fields
print '* Spatial Reference:', layer.srs
print '* Spatial Reference (Proj.4):', layer.srs.proj4

print '==============================================='

# Deeper look at France
country = layer[64]
print '* Country:', country['NAME']
print '* Number of polygons:', country.geom.geom_count
for i, poly in enumerate(country.geom):
    print ' ', '%d.' % i, poly.geom_type, poly.area
