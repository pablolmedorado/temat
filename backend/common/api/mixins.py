from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_bulk import BulkCreateModelMixin, BulkDestroyModelMixin, BulkListSerializer, BulkUpdateModelMixin

from django.utils.translation import ugettext_lazy as _

from ..decorators import atomic_transaction_singleton


# https://github.com/miki725/django-rest-framework-bulk/issues/66#issuecomment-329209982
class BulkSerializerMixin(object):
    def to_internal_value(self, data):
        ret = super(BulkSerializerMixin, self).to_internal_value(data)

        id_attr = getattr(self.Meta, "update_lookup_field", "id")
        request_method = getattr(getattr(self.context.get("view"), "request"), "method", "")

        # add update_lookup_field field back to validated data
        # since super by default strips out read-only fields
        # hence id will no longer be present in validated_data
        if all((isinstance(self.root, BulkListSerializer), id_attr, request_method in ("PUT", "PATCH"))):
            id_field = self.fields[id_attr]
            id_value = id_field.to_internal_value(id_field.get_value(data))

            ret[id_attr] = id_value

        return ret


class AtomicBulkCreateModelMixin(BulkCreateModelMixin):
    @atomic_transaction_singleton
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class AtomicBulkUpdateModelMixin(BulkUpdateModelMixin):
    @atomic_transaction_singleton
    def bulk_update(self, request, *args, **kwargs):
        return super().bulk_update(request, *args, **kwargs)


class AtomicBulkDestroyModelMixin(BulkDestroyModelMixin):
    @atomic_transaction_singleton
    def bulk_destroy(self, request, *args, **kwargs):
        return super().bulk_destroy(request, *args, **kwargs)


class OrderedMixin(object):
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
