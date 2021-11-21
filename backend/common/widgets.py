from django.utils.encoding import smart_str

from import_export.widgets import CharWidget, ManyToManyWidget
from taggit.managers import _TaggableManager


class UUIDWidget(CharWidget):
    """
    Widget for converting UUID fields.
    """

    NULL_VALUES = ["", None, "null", "NULL", "none", "NONE", "None"]

    def render(self, value, obj=None):
        if value in self.NULL_VALUES:
            return ""
        return super().render(value, obj)

    def clean(self, value, row=None, *args, **kwargs):
        if value in self.NULL_VALUES:
            return None
        return super().clean(value, row, *args, **kwargs)


class TagsWidget(ManyToManyWidget):
    """
    Widget that handles Django Taggit 'tags' field.

    :param separator: Defaults to ``','``.
    """

    def __init__(self, separator=None):
        if separator is None:
            separator = ","
        self.separator = separator
        super(ManyToManyWidget).__init__()

    def clean(self, value, row=None, *args, **kwargs):
        return value.split(self.separator) if value else []

    def render(self, value, obj=None):
        if isinstance(value, _TaggableManager):
            tags = [smart_str(getattr(obj, "name")) for obj in value.all()]
        else:
            tags = [str(v) for v in value]
        return self.separator.join(tags)
