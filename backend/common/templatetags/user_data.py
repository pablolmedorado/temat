import json

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
def user_data(user):
    user_data = {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "full_name": f"{user.first_name} {user.last_name}",
        "acronym": user.acronym,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
    }
    return mark_safe(f"<script>var djangoUserData = {json.dumps(user_data)};</script>")
