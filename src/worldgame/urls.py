from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('worldgame.views',
    url(r'^$', 'list_country', name='list_country'),

    url(r'^new/$', 'edit_country', name='new_country'),

    url(r'^(?P<id>\d+)/edit/$', 'edit_country', name='edit_country'),

    url(r'^(?P<id>\d+)/delete/$', 'edit_country',
            {'delete': True}, name='delete_country'),

    url(r'^(?P<id>\d+)/$', 'show_country', name='show_country'),
)

if settings.DEBUG:
    from django.contrib import admin
    admin.autodiscover()
    urlpatterns += patterns('',
        (r'^admin/', include(admin.site.urls)),
    )   

