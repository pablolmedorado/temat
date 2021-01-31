from rest_framework import permissions

from .serializers import BaseSerializer, BreadSerializer, BreakfastSerializer, DrinkSerializer, IngredientSerializer
from ..models import Base, Bread, Breakfast, Drink, Ingredient
from common.api.permissions import IsAdminUserOrReadOnly, IsOwnerOrReadOnly
from common.api.viewsets import AtomicFlexFieldsModelViewSet


class BreadViewSet(AtomicFlexFieldsModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsAdminUserOrReadOnly)
    queryset = Bread.objects.all()
    serializer_class = BreadSerializer
    search_fields = ("name",)
    ordering_fields = ("id", "name")
    ordering = ("name",)


class BaseViewSet(AtomicFlexFieldsModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsAdminUserOrReadOnly)
    queryset = Base.objects.all()
    serializer_class = BaseSerializer
    search_fields = ("name",)
    ordering_fields = ("id", "name")
    ordering = ("name",)


class IngredientViewSet(AtomicFlexFieldsModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsAdminUserOrReadOnly)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    search_fields = ("name",)
    ordering_fields = ("id", "name")
    ordering = ("name",)


class DrinkViewSet(AtomicFlexFieldsModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsAdminUserOrReadOnly)
    queryset = Drink.objects.all()
    serializer_class = DrinkSerializer
    search_fields = ("name",)
    ordering_fields = ("id", "name")
    ordering = ("name",)


class BreakfastViewSet(AtomicFlexFieldsModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Breakfast.objects.exclude(user__is_active=False)
    serializer_class = BreakfastSerializer
    permit_list_expands = ["user", "bread", "base", "ingredient1", "ingredient2", "drink"]
    filter_fields = ("user_id", "bread_id", "base_id", "ingredient1_id", "ingredient2_id", "drink_id")
    ordering_fields = (
        "id",
        "user__acronym",
        "bread__name",
        "base__name",
        "ingredient1__name",
        "ingredient2__name",
        "drink__name",
    )
    ordering = ("user__acronym",)

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            serializer.validated_data["user"] = self.request.user
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        if not self.request.user.is_superuser:
            serializer.validated_data["user"] = serializer.instance.user
        return super().perform_update(serializer)
