from django.utils.translation import ugettext_lazy as _

from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from users.api.serializers import UserSerializer

from ..models import Base, Bread, Breakfast, Drink, Ingredient


class BreadSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Bread
        fields = ("id", "name")
        read_only_fields = ("id",)


class BaseSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Base
        fields = ("id", "name")
        read_only_fields = ("id",)


class IngredientSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name")
        read_only_fields = ("id",)


class DrinkSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Drink
        fields = ("id", "name")
        read_only_fields = ("id",)


class BreakfastSerializer(FlexFieldsModelSerializer):
    def validate(self, data):
        data = super().validate(data)
        if data.get("ingredient1") and data.get("ingredient2") and data.get("ingredient1") == data.get("ingredient2"):
            raise serializers.ValidationError(_("No es posible seleccionar 2 veces el mismo ingrediente"))
        return data

    class Meta:
        model = Breakfast
        fields = ("id", "user", "bread", "base", "ingredient1", "ingredient2", "drink")
        read_only_fields = ("id",)
        expandable_fields = {
            "user": UserSerializer,
            "bread": BreadSerializer,
            "base": BaseSerializer,
            "ingredient1": IngredientSerializer,
            "ingredient2": IngredientSerializer,
            "drink": DrinkSerializer,
        }
