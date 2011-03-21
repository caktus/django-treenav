from django.conf.urls.defaults import *
from django.http import HttpResponse, HttpRequest
from django.template import Template, Context

def test_view(request, item_slug):
    pslug = request.POST['pslug']
    N = request.POST['N']
    t = Template('{% load treenav_tags %}{% single_level_menu pslug N %}')    
    c = Context({
        "request": request,
        "pslug": pslug,
        "N": N,
    })
    return HttpResponse(t.render(c))

urlpatterns = patterns(
    '',
    url(r'^item/(?P<item_slug>[\w-]+)/$',
        test_view, 
        name='test_view',
    ),
    (r'^old/', include('treenav.urls.undefined_url')),
)
