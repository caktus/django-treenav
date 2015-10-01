from django.apps import AppConfig
from django.db.models.signals import pre_migrate, post_migrate

from .signals import connect_post_save_handler, disconnect_post_save_handler


class TreenavConfig(AppConfig):
    name = 'treenav'

    def ready(self):
        """
        Connect post_save handler during routine operation. Disconnect it during migrations.
        """
        connect_post_save_handler()
        pre_migrate.connect(disconnect_post_save_handler)
        # now, we need to reconnect the post_save handler because unittests run
        # immediately after running migrate, in the same process
        post_migrate.connect(connect_post_save_handler)
