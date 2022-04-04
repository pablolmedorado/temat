import json

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
def backend_data(user):
    data = {
        "cvs": {
            "vendor": settings.CVS_VENDOR,
            "branch_base_url": settings.CVS_BRANCH_BASE_URL,
            "issue_base_url": settings.CVS_ISSUE_BASE_URL,
            "pull_request_base_url": settings.CVS_PULL_REQUEST_BASE_URL,
        },
        "current_user": {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "full_name": f"{user.first_name} {user.last_name}",
            "acronym": user.acronym,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "permissions": [] if user.is_superuser else sorted(list(user.get_all_permissions())),
        },
    }
    return mark_safe(f"<script>var djangoData = {json.dumps(data)};</script>")
