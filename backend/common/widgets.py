from import_export.widgets import CharWidget


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
