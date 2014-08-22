from django.conf.urls import patterns, url


urlpatterns = patterns('treenav.views',  # noqa
    url(r'item/(?P<item_slug>[\w-]+)/$',
        'treenav_undefined_url',
        name='treenav_undefined_url',
    ),
)
