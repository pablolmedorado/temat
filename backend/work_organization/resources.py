from django.contrib.auth import get_user_model

from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from .models import GreenWorkingDay, Holiday, HolidayType, SupportWorkingDay


class GreenWorkingDayResource(resources.ModelResource):
    users = Field(attribute="users", widget=ManyToManyWidget(model=get_user_model(), field="username"))

    class Meta:
        model = GreenWorkingDay
        fields = ("id", "label", "date", "users")
        export_order = ("id", "label", "date", "users")


class SupportWorkingDayResource(resources.ModelResource):
    user = Field(attribute="user", widget=ForeignKeyWidget(model=get_user_model(), field="username"))

    class Meta:
        model = SupportWorkingDay
        fields = ("id", "date", "user")
        export_order = ("id", "date", "user")


class HolidayTypeResource(resources.ModelResource):
    class Meta:
        model = HolidayType
        fields = ("id", "name", "validity", "system_slug")
        export_order = fields


class HolidayResource(resources.ModelResource):
    user = Field(attribute="user", widget=ForeignKeyWidget(model=get_user_model(), field="username"))
    type = Field(attribute="type", widget=ForeignKeyWidget(model=HolidayType, field="name"))

    class Meta:
        model = Holiday
        fields = ("id", "user", "type", "allowance_date", "planned_date", "approved", "green_working_day")
        export_order = fields
