from rest_flex_fields.views import FlexFieldsModelViewSet
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_bulk import BulkCreateModelMixin

from .mixins import FlatDatesMixin
from ..filters import GreenWorkingDayFilterSet, SupportWorkingDayFilterSet
from ..models import GreenWorkingDay, SupportWorkingDay
from ..permissions import GreenWorkingDayPermission
from ..serializers import GreenWorkingDaySerializer, SupportWorkingDaySerializer
from ..utils import green_working_day_user_chart_data, support_working_day_user_chart_data
from common.mixins import AuthorshipMixin
from common.permissions import IsAdminUserOrReadOnly


class GreenWorkingDayApi(AuthorshipMixin, FlatDatesMixin, BulkCreateModelMixin, FlexFieldsModelViewSet):
    permission_classes = (permissions.IsAuthenticated, GreenWorkingDayPermission)
    queryset = GreenWorkingDay.objects.all()
    serializer_class = GreenWorkingDaySerializer
    permit_list_expands = ["main_user", "support_user"]
    filterset_class = GreenWorkingDayFilterSet
    ordering_fields = ("date", "label", "main_user__acronym", "support_user__acronym")
    ordering = ("date",)

    @action(detail=True, methods=["PATCH"])
    def toggle_volunteer(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.volunteers.filter(id=request.user.id).exists():
            instance.volunteers.remove(request.user)
        else:
            instance.volunteers.add(request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def user_chart(self, request, *args, **kwargs):
        base_queryset = self.filter_queryset(self.get_queryset())
        chart_data = green_working_day_user_chart_data(base_queryset)
        return Response(chart_data)


class SupportWorkingDayApi(AuthorshipMixin, FlatDatesMixin, BulkCreateModelMixin, FlexFieldsModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsAdminUserOrReadOnly)
    queryset = SupportWorkingDay.objects.all()
    serializer_class = SupportWorkingDaySerializer
    permit_list_expands = ["user"]
    filterset_class = SupportWorkingDayFilterSet
    ordering_fields = ("date", "user__acronym")
    ordering = ("date",)

    @action(detail=False, methods=["GET"])
    def user_chart(self, request, *args, **kwargs):
        base_queryset = self.filter_queryset(self.get_queryset())
        chart_data = support_working_day_user_chart_data(base_queryset)
        return Response(chart_data)
