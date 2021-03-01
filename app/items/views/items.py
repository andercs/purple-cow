from http import HTTPStatus

from items.models import Item
from items.serializers import ItemsSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.response import Response

items = {}


class ItemList(CreateModelMixin, GenericAPIView):
    """
    API endpoints that allow items to be viewed, created, or deleted in bulk.
    """

    queryset = Item.objects.all()
    serializer_class = ItemsSerializer
    http_method_names = ["get", "post", "options", "delete"]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(items.values(), many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        items[item.id] = item
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTPStatus.CREATED, headers=headers)

    def delete(self, request, *args, **kwargs):
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

    def get(self, request, *args, **kwargs):
        instance = items[self.get_object().id]
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
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

    def patch(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_id = instance.id
        instance.delete()
        del items[instance_id]
        return Response(status=HTTPStatus.NO_CONTENT)
