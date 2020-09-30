from django.contrib.auth.models import Group

from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from .models import Company, User


class UserResource(resources.ModelResource):
    company = Field(attribute="company", widget=ForeignKeyWidget(model=Company, field="name"), readonly=False)
    groups = Field(attribute="groups", widget=ManyToManyWidget(model=Group, field="name"), readonly=False)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "acronym", "email", "company", "groups", "is_active")
        export_order = fields


class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company
        fields = ("id", "name", "yearly_holiday_allocation", "extra_holiday_with_green_working_days")
        export_order = fields
