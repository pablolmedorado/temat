from rest_framework import routers

from .views_api import BaseApi, BreadApi, BreakfastApi, DrinkApi, IngredientApi

app_name = "breakfasts"

router = routers.DefaultRouter()
router.register(r"bases", BaseApi, basename="base")
router.register(r"breads", BreadApi, basename="bread")
router.register(r"breakfasts", BreakfastApi, basename="breakfast")
router.register(r"drinks", DrinkApi, basename="drink")
router.register(r"ingredients", IngredientApi, basename="ingredient")

urlpatterns = router.urls
