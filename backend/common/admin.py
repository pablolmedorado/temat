from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from import_export.admin import ImportExportActionModelAdmin
from ordered_model.admin import OrderedModelAdmin
from taggit.models import Tag

from .behaviors import UUIDTaggedItem
from .models import Link, LinkType
from .resources import LinkResource, LinkTypeResource, TagResource


@admin.register(LinkType)
class LinkTypeAdmin(ImportExportActionModelAdmin, OrderedModelAdmin):
    list_display = ("id", "name", "move_up_down_links")
    list_display_links = ("name",)
    search_fields = ("name",)
    ordering = ("order",)
    fieldsets = ((_("Información básica"), {"fields": ("name",)}),)
    resource_class = LinkTypeResource


@admin.register(Link)
class LinkAdmin(ImportExportActionModelAdmin, OrderedModelAdmin):
    list_display = ("id", "name", "icon", "url", "type", "move_up_down_links")
    list_select_related = ("type",)
    search_fields = ("name", "url")
    list_filter = ("type",)
    ordering = ("type", "order")
    fieldsets = (
        (_("Información básica"), {"fields": ("name", "url")}),
        (_("Clasificación"), {"fields": ("type",)}),
        (_("Apariencia"), {"fields": ("icon",)}),
    )
    resource_class = LinkResource


class TagAdmin(ImportExportActionModelAdmin):
    list_display = ("name", "slug")
    ordering = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    resource_class = TagResource


admin.site.unregister(Tag)
admin.site.register(Tag, TagAdmin)
