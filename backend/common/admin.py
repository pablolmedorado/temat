from django.contrib import admin

from taggit.models import Tag

from .behaviors import UUIDTaggedItem


class TaggedItemInline(admin.StackedInline):
    model = UUIDTaggedItem


class TagAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    list_display = ["name", "slug"]
    ordering = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}


admin.site.unregister(Tag)
admin.site.register(Tag, TagAdmin)
