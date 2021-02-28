from items.models import BaseModel
from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        fields = ["id"]
