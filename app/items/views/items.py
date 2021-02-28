from http import HTTPStatus

from items.models import Item
from items.serializers import ItemsSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response


class ItemViewSet(viewsets.ModelViewSet):
    @action(methods=["delete"], detail=False, name="")
    def delete_all(self, request):
        self.queryset.delete()
        return Response(status=HTTPStatus.NO_CONTENT)


class ItemList(CreateModelMixin, ListModelMixin, GenericAPIView):
    """
    API endpoints that allow items to be viewed, created, or deleted in bulk.
    """

    queryset = Item.objects.all()
    serializer_class = ItemsSerializer
    http_method_names = ["get", "post", "options", "delete"]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.queryset.delete()
        return Response(status=HTTPStatus.NO_CONTENT)


class ItemDetail(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """
    API endpoints that allow items to be viewed, updated, or deleted by ID.
    """

    queryset = Item.objects.all()
    serializer_class = ItemsSerializer
    http_method_names = ["get", "put", "patch", "options", "delete"]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
