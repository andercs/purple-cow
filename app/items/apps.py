from django.apps import AppConfig


class ItemsConfig(AppConfig):
    name = "items"

    def ready(self):

        # Initialize the signals file
        from items import signals  # pylint: disable=unused-import
