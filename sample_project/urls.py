from django.conf.urls import include, url
from django.views.generic.base import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [  # noqa
    url(r'^admin/', include(admin.site.urls)),
    url(r'^treenav/', include('treenav.urls')),
    # Catch all URL to easily demonstrate treenav display
    url(r'^', TemplateView.as_view(template_name='base.html')),
]
