from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CommonConfig(AppConfig):
    name = "common"
    verbose_name = _("común")

    def ready(self):
        import common.lookups  # noqa
