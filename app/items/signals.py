from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.signals import connection_created
from django.dispatch import receiver
from items.models import Item
from items.views.items import items


@receiver(connection_created)
def load_items(connection: BaseDatabaseWrapper, **kwargs) -> None:
    """
    This function provides a way to load items into memory
    on server startup. It unregisters itself to ensure that it is only run
    once per startup.

    :param connection: a Django BaseDatabaseWrapper object
    :param kwargs: additional keyword arguments
    :return: None
    """
    for item in Item.objects.all():
        items[item.id] = item

    # We do this to ensure this runs ONLY once per startup
    connection_created.disconnect(load_items)
