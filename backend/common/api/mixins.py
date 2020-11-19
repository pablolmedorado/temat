from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_bulk import BulkCreateModelMixin, BulkDestroyModelMixin


class AtomicCreateModelMixin(mixins.CreateModelMixin):
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class AtomicBulkCreateModelMixin(BulkCreateModelMixin):
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class AtomicUpdateModelMixin(mixins.UpdateModelMixin):
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class AtomicDestroyModelMixin(mixins.DestroyModelMixin):
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class AtomicBulkDestroyModelMixin(BulkDestroyModelMixin):
    @transaction.atomic
    def bulk_destroy(self, request, *args, **kwargs):
        return super().bulk_destroy(request, *args, **kwargs)


class AtomicModelViewSetMixin(AtomicUpdateModelMixin, AtomicCreateModelMixin, AtomicDestroyModelMixin):
    """
    https://gist.github.com/prudnikov/3a968a1ee1cf9b02730cc40bc1d3d9f2
    """

    pass


class AuthorshipMixin(object):
    def perform_create(self, serializer):
        if type(serializer.validated_data) in [list, tuple]:
            for element in serializer.validated_data:
                element["creation_user"] = self.request.user
        else:
            serializer.validated_data["creation_user"] = self.request.user
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        if type(serializer.validated_data) in [list, tuple]:
            for index, element in enumerate(serializer.validated_data):
                element["creation_user"] = serializer.instance[index].creation_user
                element["modification_user"] = self.request.user
        else:
            serializer.validated_data["creation_user"] = serializer.instance.creation_user
            serializer.validated_data["modification_user"] = self.request.user
        return super().perform_update(serializer)


class OrderedMixin(object):
    def perform_create(self, serializer):
        super().perform_create(serializer)
        if "order" in self.request.data:
            serializer.instance.to(int(self.request.data.get("order")))

    def perform_update(self, serializer):
        super().perform_update(serializer)
        if "order" in self.request.data:
            serializer.instance.to(int(self.request.data.get("order")))

    @transaction.atomic
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

    @transaction.atomic
    @action(detail=True, methods=["PATCH"])
    def up(self, request, *args, **kwargs):  # noqa
        """
        Move this object up one position.
        """
        instance = self.get_object()
        instance.up()
        return Response(status=HTTP_200_OK)

    @transaction.atomic
    @action(detail=True, methods=["PATCH"])
    def down(self, request, *args, **kwargs):  # noqa
        """
        Move this object down one position.
        """
        instance = self.get_object()
        instance.down()
        return Response(status=HTTP_200_OK)

    @transaction.atomic
    @action(detail=True, methods=["PATCH"])
    def top(self, request, *args, **kwargs):
        """
        Move this object to the top of the ordered stack.
        """
        extra_update = request.data.get("extra_update", {})
        instance = self.get_object()
        instance.top(extra_update=extra_update)
        return Response(status=HTTP_200_OK)

    @transaction.atomic
    @action(detail=True, methods=["PATCH"])
    def bottom(self, request, *args, **kwargs):
        """
        Move this object to the bottom of the ordered stack.
        """
        extra_update = request.data.get("extra_update", {})
        instance = self.get_object()
        instance.bottom(extra_update=extra_update)
        return Response(status=HTTP_200_OK)
