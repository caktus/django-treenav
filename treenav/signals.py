from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db.models.signals import post_save


def treenav_save_other_object_handler(sender, instance, created, **kwargs):
    """
    This signal attempts to update the HREF of any menu items that point to
    another model object, when that objects is saved.
    """
    # import here so models don't get loaded during app loading
    from .models import MenuItem
    cache_key = 'django-treenav-menumodels'
    if sender == MenuItem:
        cache.delete(cache_key)
    menu_models = cache.get(cache_key)
    if not menu_models:
        menu_models = []
        for menu_item in MenuItem.objects.exclude(content_type__isnull=True):
            menu_models.append(menu_item.content_type.model_class())
        cache.set(cache_key, menu_models)
    # only attempt to update MenuItem if sender is known to be referenced
    if sender in menu_models:
        ct = ContentType.objects.get_for_model(sender)
        items = MenuItem.objects.filter(content_type=ct, object_id=instance.pk)
        for item in items:
            if item.href != instance.get_absolute_url():
                item.href = instance.get_absolute_url()
                item.save()


def connect_post_save_handler(**kwargs):
    """
    Connect post_save (of all models) to treenav handler above.

    Called from apps.py during app loading.
    """
    post_save.connect(treenav_save_other_object_handler)


def disconnect_post_save_handler(sender, **kwargs):
    """
    Disconnect post_save signal during migrations of any application.

    This prevents MenuItem from being accessed before it is installed in the
    database. This also means that data migrations run during other app
    migrations will NOT call the treenav handler if they have associated TreeNav
    items, they will need to be manually updated.
    """
    post_save.disconnect(treenav_save_other_object_handler)
