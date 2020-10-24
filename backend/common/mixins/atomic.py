# https://gist.github.com/prudnikov/3a968a1ee1cf9b02730cc40bc1d3d9f2

from django.db import transaction

from rest_flex_fields.views import FlexFieldsMixin
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
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
    pass


class AtomicModelViewSet(
    AtomicCreateModelMixin,
    mixins.RetrieveModelMixin,
    AtomicUpdateModelMixin,
    AtomicDestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    pass


class AtomicFlexFieldsModelViewSet(FlexFieldsMixin, AtomicModelViewSet):
    pass
