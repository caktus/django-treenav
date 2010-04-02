from treenav.models import MenuItem
from django.core.cache import cache


def treenav_active(request):
    menus = cache.get('menus')
    if not menus:
        menus = MenuItem.objects.filter(parent__isnull=True).all()
        cache.set('menus', menus)
    treenav_active = {}
    for menu in menus:
        root = menu.to_tree()
        active_leaf = root.set_active(request.META['PATH_INFO'])
        if active_leaf:
            treenav_active[menu.slug] = active_leaf.get_active_items()
    return {'treenav_active': treenav_active}
