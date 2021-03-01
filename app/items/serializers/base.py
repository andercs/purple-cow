"""Module that defines parent classes for serializers to inherit."""

from rest_framework import serializers

from items.models import BaseModel


class BaseSerializer(serializers.ModelSerializer):
    """
    Base-level serializer that provides mapping/validation for BaseModel.
    This should be treated as an "Abstract" class.

    Note: In cannot inherit from abc.ABC since it has a parent with a different
    Metaclass.
    """

    class Meta:
        model = BaseModel
        fields = ["id"]
