from django.conf.urls import url

from .views import treenav_undefined_url

urlpatterns = [
    url(r'item/(?P<item_slug>[\w-]+)/$', treenav_undefined_url, name='treenav_undefined_url'),
]
