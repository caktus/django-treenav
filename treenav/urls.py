try:
    from django.conf.urls import patterns, url
except ImportError:
    # Django <= 1.3
    from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('treenav.views',
    url(r'item/(?P<item_slug>[\w-]+)/$',
        'treenav_undefined_url', 
        name='treenav_undefined_url',
    ),
)
