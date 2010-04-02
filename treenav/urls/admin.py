from django.conf.urls.defaults import *


urlpatterns = patterns('treenav.views',
    url(r'^refresh-hrefs/$',
        'treenav_refresh_hrefs', 
        name='treenav_refresh_hrefs',
    ),
    url(r'^clean-cache/$',
        'treenav_refresh_hrefs', 
        name='treenav_clean_cache',
    ),
)
