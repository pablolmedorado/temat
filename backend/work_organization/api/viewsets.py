from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db import transaction
from django.db.models import Count, F, Min
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from notifications.signals import notify
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_bulk import BulkCreateModelMixin

from .filtersets import GreenWorkingDayFilterSet, HolidayFilterSet, SupportWorkingDayFilterSet
from .mixins import FlatDatesMixin
from .permissions import GreenWorkingDayPermission, HolidayPermission
from .serializers import (
    GreenWorkingDaySerializer,
    HolidaySerializer,
    HolidayTypeSerializer,
    SupportWorkingDaySerializer,
)
from ..models import GreenWorkingDay, Holiday, HolidayType, SupportWorkingDay
from ..utils import green_working_day_user_chart_data, support_working_day_user_chart_data, user_availability_chart_data
from common.api.mixins import AtomicBulkCreateModelMixin
from common.api.permissions import HasDjangoPermissionOrReadOnly
from common.api.viewsets import AtomicFlexFieldsModelViewSet


class GreenWorkingDayViewSet(FlatDatesMixin, AtomicBulkCreateModelMixin, AtomicFlexFieldsModelViewSet):
    permission_classes = (permissions.IsAuthenticated, GreenWorkingDayPermission)
    queryset = GreenWorkingDay.objects.all()
    serializer_class = GreenWorkingDaySerializer
    permit_list_expands = ["main_user", "support_user"]
    filterset_class = GreenWorkingDayFilterSet
    ordering_fields = ("date", "label", "main_user__acronym", "support_user__acronym")
    ordering = ("date",)

    @transaction.atomic
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


class SupportWorkingDayViewSet(FlatDatesMixin, BulkCreateModelMixin, AtomicFlexFieldsModelViewSet):
    permission_classes = (permissions.IsAuthenticated, HasDjangoPermissionOrReadOnly)
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


class HolidayTypeViewSet(AtomicFlexFieldsModelViewSet):
    permission_classes = (permissions.IsAuthenticated, HasDjangoPermissionOrReadOnly)
    queryset = HolidayType.objects.all()
    serializer_class = HolidayTypeSerializer
    filterset_fields = ("system_slug",)
    search_fields = ("name",)
    ordering_fields = ("id", "name", "system_slug")
    ordering = ("name",)


class HolidayViewSet(FlatDatesMixin, AtomicFlexFieldsModelViewSet):
    permission_classes = (permissions.IsAuthenticated, HolidayPermission)
    queryset = Holiday.objects.with_expiration_date()
    serializer_class = HolidaySerializer
    permit_list_expands = ["user", "type"]
    filterset_class = HolidayFilterSet
    ordering_fields = (
        "user__acronym",
        "allowance_date",
        "planned_date",
        "approved",
        "creation_datetime",
        "expiration_date",
    )
    ordering = ("-planned_date",)

    flat_dates_field = "planned_date"

    @transaction.atomic
    @action(detail=False, methods=["POST"])
    def request(self, request, *args, **kwargs):
        if "dates" not in request.data:
            return Response(_("El parámetro 'dates' es obligatorio"), status=status.HTTP_400_BAD_REQUEST)
        try:
            requested_dates = [date.fromisoformat(requested_date) for requested_date in request.data.get("dates", [])]
        except ValueError:
            return Response(_("Alguna de las fechas proporcionadas no es válida"), status=status.HTTP_400_BAD_REQUEST)

        base_queryset = self.get_queryset()
        if base_queryset.filter(user=request.user, planned_date__in=requested_dates).exists():
            return Response(
                _("El usuario ya tiene planeadas vacaciones en alguna de las fechas proporcionadas"),
                status=status.HTTP_400_BAD_REQUEST,
            )

        available_holidays_queryset = base_queryset.filter(
            user=request.user,
            planned_date__isnull=True,
            allowance_date__lte=timezone.now(),
            expiration_date_annotation__gte=timezone.now(),
            approved__isnull=True,
        ).order_by("expiration_date_annotation")
        available_holidays_count = available_holidays_queryset.count()
        if len(requested_dates) > available_holidays_count:
            return Response(
                _("El usuario no tiene días de vacaciones suficientes. Disponibles: {holidays_count}").format(
                    holidays_count=available_holidays_count
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        available_holidays_min_date = available_holidays_queryset.aggregate(Min("allowance_date"))
        for requested_date in requested_dates:
            if requested_date < available_holidays_min_date["allowance_date__min"]:
                return Response(
                    _("Alguna de las fechas solicitadas es anterior a la mínima permitida: {min_date}").format(
                        min_date=available_holidays_min_date["allowance_date__min"]
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )

        holiday_pks = []
        for requested_date in requested_dates:
            holiday = available_holidays_queryset.first()
            if holiday:
                base_queryset.filter(pk=holiday.pk).update(planned_date=requested_date)
                holiday_pks.append(holiday.pk)

        global_admin_users = get_user_model().objects.admins().exclude(pk=request.user.pk).order_by()
        change_holidays_permission = Permission.objects.get_by_natural_key(
            "change_holiday", "work_organization", "holiday"
        )
        holiday_admin_users = change_holidays_permission.user_set.exclude(pk=request.user.pk).order_by()
        notify.send(
            sender=request.user,
            recipient=global_admin_users.union(holiday_admin_users),
            verb=f"ha solicitado {len(requested_dates)} días de vacaciones",
        )

        serializer = self.get_serializer(base_queryset.filter(pk__in=holiday_pks), many=True)
        return Response(serializer.data)

    @transaction.atomic
    @action(detail=True, methods=["PATCH"])
    def cancel(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {"planned_date": None, "approved": None}
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def summary(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        summary = (
            queryset.exclude(planned_date__isnull=True)
            .order_by("planned_date")
            .values(date=F("planned_date"))
            .annotate(users=Count("id"))
        )
        return Response(summary)

    @action(detail=False, methods=["GET"])
    def user_availability_chart(self, request, *args, **kwargs):
        base_queryset = self.filter_queryset(self.get_queryset())
        chart_data = user_availability_chart_data(base_queryset)
        return Response(chart_data)
