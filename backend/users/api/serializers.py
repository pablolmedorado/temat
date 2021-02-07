from django.contrib.auth.models import Group

from rest_flex_fields import FlexFieldsModelSerializer

from ..models import Company, User


class GroupSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "name")
        read_only_fields = fields


class CompanySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name")
        read_only_fields = fields


class UserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "acronym",
            "company",
            "groups",
            "is_staff",
            "is_superuser",
            "is_active",
        )
        read_only_fields = fields
        expandable_fields = {
            "company": CompanySerializer,
            "groups": (GroupSerializer, {"many": True}),
        }
