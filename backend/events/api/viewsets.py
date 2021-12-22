from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Count, F
from django.db.models.functions import TruncDay
from django.http import HttpResponse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from rest_flex_fields.views import FlexFieldsModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .filtersets import EventFilterSet
from .serializers import EventSerializer, EventTypeSerializer
from ..models import Event, EventType
from ..utils import monthly_chart_data
from common.api.permissions import HasDjangoPermissionOrReadOnly, IsOwnerOrReadOnly


class EventTypeViewSet(FlexFieldsModelViewSet):
    permission_classes = (permissions.IsAuthenticated, HasDjangoPermissionOrReadOnly)
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer
    filterset_fields = ("important", "system_slug")
    search_fields = ("name",)
    ordering_fields = ("id", "name", "important", "system_slug")
    ordering = ("name",)


class EventViewSet(FlexFieldsModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = EventSerializer
    permit_list_expands = ["attendees", "type", "groups", "tags"]
    filterset_class = EventFilterSet
    search_fields = ("name", "details")
    ordering_fields = ("name", "type", "start_datetime", "visibility")
    ordering = ("-start_datetime",)

    def get_queryset(self, *args, **kwargs):
        queryset = Event.objects.all().distinct()
        if self.action == "my_important_dates":
            return queryset.important_by_attendee(self.request.user)
        if self.action.endswith("_chart"):
            return queryset.exclude(type__system_slug__isnull=False)
        if self.action == "my_events":
            return queryset.by_attendee(self.request.user).prefetch_related("attendees", "groups", "tags")
        return queryset.by_user(self.request.user).prefetch_related("attendees", "groups", "tags")

    @action(detail=False, methods=["GET"])
    def my_events(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=False, methods=["GET"])
    def my_important_dates(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        important_dates = (
            queryset.order_by("start_datetime")
            .annotate(date=TruncDay("start_datetime"))
            .values_list("date", flat=True)
            .distinct()
        )
        return Response([item.date() for item in important_dates])

    @action(detail=False, methods=["GET"])
    def type_pie_chart(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        chart_data = (
            EventType.objects.filter(events__in=queryset)
            .distinct()
            .annotate(y=Count("events"))
            .values("name", "y", color=F("colour"))
        )
        return Response(chart_data)

    @action(detail=False, methods=["GET"])
    def attendee_packedbubble_chart(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        chart_data = {
            "series": [
                {
                    "name": _("Usuarios"),
                    "data": get_user_model()
                    .objects.active()
                    .filter(events__in=queryset)
                    .distinct()
                    .annotate(value=Count("events"))
                    .values("value", name=F("acronym")),
                },
                {
                    "name": _("Grupos"),
                    "data": Group.objects.filter(events__in=queryset)
                    .distinct()
                    .annotate(value=Count("events"))
                    .values("name", "value"),
                },
            ]
        }
        return Response(chart_data)

    @action(detail=False, methods=["GET"])
    def monthly_chart(self, request, *args, **kwargs):
        base_queryset = self.filter_queryset(self.get_queryset())
        chart_data = monthly_chart_data(base_queryset)
        return Response(chart_data)

    @action(detail=False, methods=["GET"])
    def ical(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().select_related("type", "creation_user"))
        event_list = self.paginate_queryset(queryset)
        if event_list is None:
            event_list = list(set(queryset))
        now = timezone.now().strftime("%Y%m%d%H%M%S")
        response = HttpResponse(Event.from_list_to_icalendar(event_list).to_ical(), content_type="text/calendar")
        response["Content-Disposition"] = f"attachment; filename=TeMaT_events_{now}.ics"
        return response
