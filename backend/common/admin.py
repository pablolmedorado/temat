from import_export.admin import ImportExportActionModelAdmin
from ordered_model.admin import OrderedModelAdmin
from taggit.models import Tag as TaggitTag

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Link, LinkType, Tag
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


@admin.register(Tag)
class TagAdmin(ImportExportActionModelAdmin):
    list_display = (
        "name",
        "slug",
        "icon",
        "colored_colour",
    )
    search_fields = ("name",)
    ordering = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        (_("Información básica"), {"fields": ("name", "slug")}),
        (_("Apariencia"), {"fields": ("colour", "icon")}),
    )
    resource_class = TagResource


admin.site.unregister(TaggitTag)
