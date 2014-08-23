from django.http import Http404
from django.shortcuts import get_object_or_404

from treenav import models as treenav


def treenav_undefined_url(request, item_slug):
    """
    Sample view demonstrating that you can provide custom handlers for
    undefined menu items on a per-item basis.
    """
    item = get_object_or_404(treenav.MenuItem, slug=item_slug)  # noqa
    # do something with item here and return an HttpResponseRedirect
    raise Http404
