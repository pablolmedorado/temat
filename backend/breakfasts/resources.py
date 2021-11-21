from django.contrib.auth import get_user_model

from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import Base, Bread, Breakfast, Drink, Ingredient


class BreadResource(resources.ModelResource):
    class Meta:
        model = Bread
        fields = ("id", "name")
        export_order = fields


class BaseResource(resources.ModelResource):
    class Meta:
        model = Base
        fields = ("id", "name")
        export_order = fields


class IngredientResource(resources.ModelResource):
    class Meta:
        model = Ingredient
        fields = ("id", "name")
        export_order = fields


class DrinkResource(resources.ModelResource):
    class Meta:
        model = Drink
        fields = ("id", "name")
        export_order = fields


class BreakfastResource(resources.ModelResource):
    user = Field(attribute="user", widget=ForeignKeyWidget(model=get_user_model(), field="name"))
    bread = Field(attribute="bread", widget=ForeignKeyWidget(model=Bread, field="name"))
    base = Field(attribute="base", widget=ForeignKeyWidget(model=Base, field="name"))
    ingredient1 = Field(attribute="ingredient1", widget=ForeignKeyWidget(model=Ingredient, field="name"))
    ingredient2 = Field(attribute="ingredient2", widget=ForeignKeyWidget(model=Ingredient, field="name"))
    drink = Field(attribute="drink", widget=ForeignKeyWidget(model=Drink, field="name"))

    class Meta:
        model = Breakfast
        fields = ("id", "user", "bread", "base", "ingredient1", "ingredient2", "drink")
        export_order = fields
