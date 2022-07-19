from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.utils.translation import ugettext_lazy as _

from common.api.mixins import BulkSerializerMixin
from users.api.serializers import UserSerializer
from ..models import GreenWorkingDay, Holiday, HolidayType, SupportWorkingDay


class GreenWorkingDaySerializer(BulkSerializerMixin, FlexFieldsModelSerializer):
    date = serializers.DateField(validators=[UniqueValidator(queryset=GreenWorkingDay.objects.all())])

    class Meta:
        model = GreenWorkingDay
        fields = (
            "id",
            "label",
            "date",
            "users",
            "volunteers",
            "creation_datetime",
            "creation_user",
            "modification_datetime",
            "modification_user",
        )
        read_only_fields = ("id", "creation_datetime", "creation_user", "modification_datetime", "modification_user")
        expandable_fields = {
            "users": (UserSerializer, {"many": True}),
            "volunteers": (UserSerializer, {"many": True}),
        }


class SupportWorkingDaySerializer(BulkSerializerMixin, FlexFieldsModelSerializer):
    date = serializers.DateField(validators=[UniqueValidator(queryset=SupportWorkingDay.objects.all())])

    class Meta:
        model = SupportWorkingDay
        fields = (
            "id",
            "date",
            "user",
            "creation_datetime",
            "creation_user",
            "modification_datetime",
            "modification_user",
        )
        read_only_fields = ("id", "creation_datetime", "creation_user", "modification_datetime", "modification_user")
        expandable_fields = {"user": (UserSerializer, {"many": False})}


class HolidayTypeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = HolidayType
        fields = ("id", "name", "validity", "system_slug")
        read_only_fields = ("id",)


class HolidaySerializer(FlexFieldsModelSerializer):
    def validate(self, data):
        data = super().validate(data)
        if data.get("planned_date") and data.get("planned_date") < data.get("allowance_date"):
            raise serializers.ValidationError(
                _("No es posible usar un día de vacaciones para una fecha anterior a la de concesión")
            )
        return data

    class Meta:
        model = Holiday
        fields = (
            "id",
            "user",
            "type",
            "allowance_date",
            "planned_date",
            "approved",
            "expiration_date",
            "creation_datetime",
            "creation_user",
            "modification_datetime",
            "modification_user",
        )
        read_only_fields = (
            "expiration_date",
            "creation_datetime",
            "creation_user",
            "modification_datetime",
            "modification_user",
        )
        expandable_fields = {
            "user": UserSerializer,
            "type": HolidayTypeSerializer,
        }
