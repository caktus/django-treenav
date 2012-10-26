try:
    from django.conf.urls import patterns, url
except ImportError:
    # Django <= 1.3
    from django.conf.urls.defaults import patterns, url


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
