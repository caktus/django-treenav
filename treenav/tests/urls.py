from django.contrib import admin
from django.http import HttpResponse, HttpResponseNotFound
from django.template import Context, Template
from django.urls import include, path

import treenav.urls

from ..admin import MenuItemAdmin
from ..models import MenuItem

admin.autodiscover()
# create a second Admin site and register MenuItem against it
site2 = admin.AdminSite(name="admin2")
site2.register(MenuItem, MenuItemAdmin)


def test_view(request, item_slug):
    pslug = request.POST["pslug"]
    N = request.POST["N"]
    t = Template("{% load treenav_tags %}{% single_level_menu pslug N %}")
    c = Context(
        {
            "request": request,
            "pslug": pslug,
            "N": N,
        }
    )
    return HttpResponse(t.render(c))


def test_404(request, exception=None):
    return HttpResponseNotFound()


handler404 = test_404  # noqa


urlpatterns = [
    path("admin/", admin.site.urls),
    path("admin2/", site2.urls),
    path("item/<slug:item_slug>/$", test_view, name="test_view"),
    path("old/", include(treenav.urls)),
]
