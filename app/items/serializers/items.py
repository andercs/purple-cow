"""Module that defines Serializers for item-related models."""

from items.models import Item
from items.serializers.base import BaseSerializer


class ItemsSerializer(BaseSerializer):
    """
    Serializer that provides serialization/deserialization and validation
    for Item models.
    """

    class Meta(BaseSerializer.Meta):
        model = Item
        fields = BaseSerializer.Meta.fields + ["name"]
