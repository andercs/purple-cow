from http import HTTPStatus

from items.models import Item
from items.serializers import ItemsSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows items to be viewed or edited.
    """

    queryset = Item.objects.all()
    serializer_class = ItemsSerializer

    @action(methods=["delete"], detail=False, name="")
    def delete_all(self, request):
        self.queryset.delete()
        return Response(status=HTTPStatus.NO_CONTENT)
