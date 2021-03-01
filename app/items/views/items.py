"""Module that defines views for the item-related models."""

from http import HTTPStatus

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response

from items.models import Item
from items.serializers import ItemsSerializer

# Define a dictionary for storing "Item" objects in memory, per the client's request
items = {}


class ItemList(CreateModelMixin, GenericAPIView):
    """
    API endpoints that allow items to be listed, created, or bulk deleted.
    """

    queryset = Item.objects.all()
    serializer_class = ItemsSerializer
    http_method_names = ["get", "post", "options", "delete"]

    def get(self, request: Request, *args, **kwargs) -> Response:
        """Method to retrieve a listing of all available items."""
        serializer = self.get_serializer(items.values(), many=True)
        return Response(serializer.data)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """Method to create a new item."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        items[item.id] = item
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTPStatus.CREATED, headers=headers)

    def delete(self, request, *args, **kwargs) -> Response:
        """Method to delete all available items."""
        self.queryset.delete()
        items.clear()
        return Response(status=HTTPStatus.NO_CONTENT)


class ItemDetail(UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """
    API endpoints that allow items to be viewed, updated, or deleted by ID.
    """

    queryset = Item.objects.all()
    serializer_class = ItemsSerializer
    http_method_names = ["get", "put", "patch", "options", "delete"]

    def get(self, request: Request, *args, **kwargs) -> Response:
        """Method to retrieve a single item by ID."""
        instance = items[self.get_object().id]
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def put(self, request: Request, *args, **kwargs) -> Response:
        """Method to update a single item by ID."""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        items[item.id] = item

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def patch(self, request: Request, *args, **kwargs) -> Response:
        """Method to perform a partial update of a single item by ID."""
        kwargs["partial"] = True
        return self.put(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """Method to delete a single item by ID."""
        instance = self.get_object()
        instance_id = instance.id
        instance.delete()
        del items[instance_id]
        return Response(status=HTTPStatus.NO_CONTENT)
