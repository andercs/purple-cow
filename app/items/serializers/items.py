from items.models import Item
from items.serializers.base import BaseSerializer


class ItemsSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Item
        fields = BaseSerializer.Meta.fields + ["name"]
