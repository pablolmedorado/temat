from django.utils.translation import ugettext_lazy as _

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_bulk import BulkCreateModelMixin, BulkDestroyModelMixin

from ..decorators import atomic_transaction_singleton


class AtomicBulkCreateModelMixin(BulkCreateModelMixin):
    @atomic_transaction_singleton
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class AtomicBulkDestroyModelMixin(BulkDestroyModelMixin):
    @atomic_transaction_singleton
    def bulk_destroy(self, request, *args, **kwargs):
        return super().bulk_destroy(request, *args, **kwargs)


class OrderedMixin(object):
    def perform_create(self, serializer):
        super().perform_create(serializer)
        if "order" in self.request.data:
            serializer.instance.to(int(self.request.data.get("order")))

    def perform_update(self, serializer):
        super().perform_update(serializer)
        if "order" in self.request.data:
            serializer.instance.to(int(self.request.data.get("order")))

    @atomic_transaction_singleton
    @action(detail=True, methods=["PATCH"])
    def to(self, request, *args, **kwargs):  # noqa
        """
        Move object to a certain position, updating all affected objects to move accordingly up or down.
        """
        if "order" not in request.data:
            return Response({"detail": _("El parámetro orden es obligatorio")}, status=HTTP_400_BAD_REQUEST)
        extra_update = request.data.get("extra_update", {})
        instance = self.get_object()
        instance.to(int(self.request.data.get("order")), extra_update=extra_update)
        return Response(status=HTTP_200_OK)

    @atomic_transaction_singleton
    @action(detail=True, methods=["PATCH"])
    def up(self, request, *args, **kwargs):  # noqa
        """
        Move this object up one position.
        """
        instance = self.get_object()
        instance.up()
        return Response(status=HTTP_200_OK)

    @atomic_transaction_singleton
    @action(detail=True, methods=["PATCH"])
    def down(self, request, *args, **kwargs):  # noqa
        """
        Move this object down one position.
        """
        instance = self.get_object()
        instance.down()
        return Response(status=HTTP_200_OK)

    @atomic_transaction_singleton
    @action(detail=True, methods=["PATCH"])
    def top(self, request, *args, **kwargs):
        """
        Move this object to the top of the ordered stack.
        """
        extra_update = request.data.get("extra_update", {})
        instance = self.get_object()
        instance.top(extra_update=extra_update)
        return Response(status=HTTP_200_OK)

    @atomic_transaction_singleton
    @action(detail=True, methods=["PATCH"])
    def bottom(self, request, *args, **kwargs):
        """
        Move this object to the bottom of the ordered stack.
        """
        extra_update = request.data.get("extra_update", {})
        instance = self.get_object()
        instance.bottom(extra_update=extra_update)
        return Response(status=HTTP_200_OK)
