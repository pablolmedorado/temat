from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ScrumConfig(AppConfig):
    name = "scrum"
    verbose_name = _("scrum")

    def ready(self):
        import scrum.signals  # noqa
