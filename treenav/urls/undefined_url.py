from django.conf.urls.defaults import *


urlpatterns = patterns('treenav.views',
    url(r'item/(?P<item_slug>[\w-]+)/$',
        'treenav_undefined_url', 
        name='treenav_undefined_url',
    ),
)
