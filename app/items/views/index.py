"""Module that defines root level views for the API."""

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(["GET"])
def api_root(request: Request, format=None) -> Response:
    """Method that provides an index of the 'items' application API."""
    return Response(
        {
            "item": reverse("item-list", request=request, format=format),
        }
    )
