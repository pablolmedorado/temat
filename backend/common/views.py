from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ClientSPA(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
