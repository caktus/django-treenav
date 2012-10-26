from django.conf.urls.defaults import patterns, include, url
from django.views.generic.base import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sample_project.views.home', name='home'),
    # url(r'^sample_project/', include('sample_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^treenav/', include('treenav.urls')),
    # Catch all URL to easily demonstrate treenav display
    url(r'^', TemplateView.as_view(template_name='base.html')),
)
