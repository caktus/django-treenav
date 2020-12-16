from django.apps import AppConfig, apps
from django.db.models.signals import post_migrate, pre_migrate

from .signals import connect_post_save_handler, disconnect_post_save_handler


class TreenavConfig(AppConfig):
    name = "treenav"

    def ready(self):
        """
        Connect post_save handler during routine operation. Disconnect it during migrations.
        """
        connect_post_save_handler()
        pre_migrate.connect(disconnect_post_save_handler)
        # now, we need to reconnect the post_save handler because unittests run
        # immediately after running migrate, in the same process
        post_migrate.connect(connect_post_save_handler)


def setup_test_app(package, label=None):
    """
    Setup a Django test app for the provided package to allow test models
    tables to be created if the containing app has migrations.

    This function should be called from app.tests __init__ module and pass
    along __package__.

    link: https://code.djangoproject.com/ticket/7835#comment:46
    """
    app_config = AppConfig.create(package)
    app_config.apps = apps
    if label is None:
        containing_app_config = apps.get_containing_app_config(package)
        label = f"{containing_app_config.label}_tests"
    if label in apps.app_configs:
        raise ValueError(f"There's already an app registered with the '{label}' label.")
    app_config.label = label
    apps.app_configs[app_config.label] = app_config
    app_config.import_models()
    apps.clear_cache()
