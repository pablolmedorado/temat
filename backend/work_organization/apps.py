from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class WorkOrganizationConfig(AppConfig):
    name = "work_organization"
    verbose_name = _("organización del trabajo")

    def ready(self):
        import work_organization.signals  # noqa
