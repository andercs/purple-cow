"""This module defines items-related models."""

from django.db import models

from items.models.base import BaseModel


class Item(BaseModel):
    """
    Model that holds information about Items.
    """

    name = models.TextField(help_text="Name of item")

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self) -> str:
        """
        This method returns the string representation of an instance.

        :return: str
        """
        return str(self.name)
