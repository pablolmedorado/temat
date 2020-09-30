from django.utils.translation import ugettext_lazy as _

from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_bulk import BulkSerializerMixin

from users.serializers import UserSerializer
from ..models import GreenWorkingDay, SupportWorkingDay


class GreenWorkingDaySerializer(BulkSerializerMixin, FlexFieldsModelSerializer):
    date = serializers.DateField(validators=[UniqueValidator(queryset=GreenWorkingDay.objects.all())])

    def validate(self, data):
        data = super().validate(data)
        if data.get("main_user") and data.get("support_user") and data.get("main_user") == data.get("support_user"):
            raise serializers.ValidationError(_("No es posible asignar el rol principal y de apoyo al mismo usuario"))
        return data

    class Meta:
        model = GreenWorkingDay
        fields = (
            "id",
            "label",
            "date",
            "main_user",
            "support_user",
            "volunteers",
            "creation_datetime",
            "creation_user",
            "modification_datetime",
            "modification_user",
        )
        read_only_fields = ("id", "creation_datetime", "creation_user", "modification_datetime", "modification_user")
        expandable_fields = {
            "main_user": UserSerializer,
            "support_user": UserSerializer,
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
