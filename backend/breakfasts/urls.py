from rest_framework import routers

from .api.viewsets import BaseViewSet, BreadViewSet, BreakfastViewSet, DrinkViewSet, IngredientViewSet

app_name = "breakfasts"

router = routers.DefaultRouter()
router.register(r"bases", BaseViewSet, basename="base")
router.register(r"breads", BreadViewSet, basename="bread")
router.register(r"breakfasts", BreakfastViewSet, basename="breakfast")
router.register(r"drinks", DrinkViewSet, basename="drink")
router.register(r"ingredients", IngredientViewSet, basename="ingredient")

urlpatterns = router.urls
