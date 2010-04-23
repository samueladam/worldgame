from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('worldgame.views',
    url(r'^$', 'question', name='question'),

    url(r'^country/(?P<name>.*)/$', 'answer', name='answer'),

    url(r'^reset/$', 'reset_score', name='reset_score'),

    url(r'^highscore/$', 'highscore', name='highscore'),
)

if settings.DEBUG:
    from django.contrib import admin
    admin.autodiscover()
    urlpatterns += patterns('',
        (r'^admin/', include(admin.site.urls)),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
                                  {'document_root': settings.MEDIA_ROOT}),
    )

