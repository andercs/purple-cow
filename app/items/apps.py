"""This module provides the Django AppConfig for the 'items' application."""

from django.apps import AppConfig

from items.constants import APP_NAME


class ItemsConfig(AppConfig):
    """
    AppConfig for the "Items" application.
    """

    name = APP_NAME

    def ready(self) -> None:
        """
        This method performs any additional initialization expected for the "items"
        application.
        """

        # Initialize the signals for this application.
        # Note: this is NOT actually an unused import
        from items import signals
