"""Module provides Django-based signals to the 'items' application"""

from django.apps.registry import apps
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.signals import connection_created
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.state import ProjectState
from django.dispatch import receiver

from items.constants import APP_NAME
from items.models import Item
from items.views.items import items


@receiver(connection_created)
def load_items(connection: BaseDatabaseWrapper, **kwargs) -> None:
    """
    This function provides a way to load items into memory
    on server startup from the target database.

    It unregisters itself to ensure that it is only run
    once per startup.

    :param connection: a Django BaseDatabaseWrapper object
    :param kwargs: additional keyword arguments
    :return: None
    """
    connection = connections[DEFAULT_DB_ALIAS]
    connection.prepare_database()
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    autodetector = MigrationAutodetector(
        executor.loader.project_state(),
        ProjectState.from_apps(apps),
    )

    unmade_migrations = autodetector.changes(graph=executor.loader.graph)
    unrun_migrations = executor.migration_plan(targets)

    all_migrations_run = True
    # If there are any unmade migrations, we can't safely load the items into memory
    for app in unmade_migrations:
        if APP_NAME in str(app):
            print("Can't load items. Detected unmade migrations.")
            all_migrations_run = False
            break

    # If there aren't unmade migrations, check if any migrations still need applied
    if all_migrations_run:
        for migration, _ in unrun_migrations:
            if APP_NAME in str(migration):
                print("Can't load items. Migrations need applied.")
                all_migrations_run = False
                break

    # If all migrations are run and there aren't unmade migrations, we load the items into memory
    if all_migrations_run:
        for item in Item.objects.all():
            items[item.id] = item

    # We do this to ensure this runs ONLY once per startup
    connection_created.disconnect(load_items)
