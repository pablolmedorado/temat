from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


class AtomicMixin(object):
    """
    Ensures we rollback db transactions on exceptions.
    Idea from https://github.com/tomchristie/django-rest-framework/pull/1204
    """

    @transaction.atomic()
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def handle_exception(self, *args, **kwargs):
        response = super().handle_exception(*args, **kwargs)

        if getattr(response, "exception"):
            # We've suppressed the exception but still need to rollback any transaction.
            transaction.set_rollback(True)

        return response


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

    @action(detail=True, methods=["PATCH"])
    def up(self, request, *args, **kwargs):  # noqa
        """
        Move this object up one position.
        """
        instance = self.get_object()
        instance.up()
        return Response(status=HTTP_200_OK)

    @action(detail=True, methods=["PATCH"])
    def down(self, request, *args, **kwargs):  # noqa
        """
        Move this object down one position.
        """
        instance = self.get_object()
        instance.down()
        return Response(status=HTTP_200_OK)

    @action(detail=True, methods=["PATCH"])
    def top(self, request, *args, **kwargs):
        """
        Move this object to the top of the ordered stack.
        """
        extra_update = request.data.get("extra_update", {})
        instance = self.get_object()
        instance.top(extra_update=extra_update)
        return Response(status=HTTP_200_OK)

    @action(detail=True, methods=["PATCH"])
    def bottom(self, request, *args, **kwargs):
        """
        Move this object to the bottom of the ordered stack.
        """
        extra_update = request.data.get("extra_update", {})
        instance = self.get_object()
        instance.bottom(extra_update=extra_update)
        return Response(status=HTTP_200_OK)
