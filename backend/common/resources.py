from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import Link, LinkType, Tag


class LinkResource(resources.ModelResource):
    type = Field(attribute="type", widget=ForeignKeyWidget(model=LinkType, field="name"))

    class Meta:
        model = Link
        fields = ("id", "name", "icon", "url", "type", "order")
        export_order = fields


class LinkTypeResource(resources.ModelResource):
    class Meta:
        model = LinkType
        fields = ("id", "name", "order")
        export_order = fields


class TagResource(resources.ModelResource):
    class Meta:
        model = Tag
        fields = ("id", "name", "slug", "colour", "icon")
        export_order = fields
