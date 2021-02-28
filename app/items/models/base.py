"""This module provides a base model class, along with related classes."""

import uuid

from django.db import models


class BaseModel(models.Model):
    """
    Base model class.

    This class stores in a single location the basic information that all models should hold.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    updated = models.DateTimeField(auto_now=True, null=False, blank=False)

    class Meta:
        abstract = True
