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
    user = Field(attribute="user", widget=ForeignKeyWidget(model=get_user_model(), field="name"), readonly=False)
    bread = Field(attribute="bread", widget=ForeignKeyWidget(model=Bread, field="name"), readonly=False)
    base = Field(attribute="base", widget=ForeignKeyWidget(model=Base, field="name"), readonly=False)
    ingredient1 = Field(
        attribute="ingredient1", widget=ForeignKeyWidget(model=Ingredient, field="name"), readonly=False
    )
    ingredient2 = Field(
        attribute="ingredient2", widget=ForeignKeyWidget(model=Ingredient, field="name"), readonly=False
    )
    drink = Field(attribute="drink", widget=ForeignKeyWidget(model=Drink, field="name"), readonly=False)

    class Meta:
        model = Breakfast
        fields = ("id", "user", "bread", "base", "ingredient1", "ingredient2", "drink")
        export_order = fields
