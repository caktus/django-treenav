from django.urls import path

from .views import treenav_undefined_url

urlpatterns = [
    path("item/<slug:item_slug>/", treenav_undefined_url, name="treenav_undefined_url"),
]
