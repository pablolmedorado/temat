from import_export.admin import ImportExportActionModelAdmin

from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import Base, Bread, Breakfast, Drink, Ingredient
from .resources import BaseResource, BreadResource, BreakfastResource, DrinkResource, IngredientResource


@admin.register(Bread)
class BreadAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    resource_class = BreadResource


@admin.register(Base)
class BaseAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    resource_class = BaseResource


@admin.register(Ingredient)
class IngredientAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    resource_class = IngredientResource


@admin.register(Drink)
class DrinkAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    resource_class = DrinkResource


@admin.register(Breakfast)
class BreakfastAdmin(ImportExportActionModelAdmin):
    list_display = ("user", "bread", "base", "ingredient1", "ingredient2", "drink")
    list_display_links = ("user",)
    list_select_related = ("bread", "base", "ingredient1", "ingredient2", "drink")
    search_fields = ("bread__name", "base__name", "ingredient1__name", "ingredient2__name", "drink__name")
    list_filter = ("user", "bread", "base", "ingredient1", "ingredient2", "drink")
    ordering = ("user",)
    fieldsets = (
        (_("Usuario"), {"fields": ("user",)}),
        (_("Principal"), {"fields": ("bread", "base")}),
        (_("Ingredientes"), {"fields": ("ingredient1", "ingredient2")}),
        (_("Bebida"), {"fields": ("drink",)}),
    )
    resource_class = BreakfastResource
