from treenav.models import MenuItem

def treenav_active(request):
    menus = MenuItem.objects.filter(parent__isnull=True).all()
    treenav_active = {}
    for menu in menus:
        root = menu.to_tree()
        active_leaf = root.set_active(request.META['PATH_INFO'])
        treenav_active[menu.slug] = active_leaf.get_active_items()
    return {'treenav_active': treenav_active }
     
