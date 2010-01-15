from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from treenav import models as treenav


def treenav_undefined_url(request, item_slug):
    """
    Sample view demonstrating that you can provide custom handlers for
    undefined menu items on a per-item basis.
    """
    item = get_object_or_404(treenav.MenuItem, slug=item_slug)
    # do something with item here and return an HttpResponseRedirect
    raise Http404


def treenav_refresh_hrefs(request):
    """
    Refresh all the cached menu item HREFs in the database.
    """
    for item in treenav.MenuItem.objects.all():
        item.save() # refreshes the HREF
    request.user.message_set.create(message='Menu item HREFs refreshed '
                                    'successfully.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/admin/'))
