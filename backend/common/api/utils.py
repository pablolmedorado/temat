from rest_framework.generics import GenericAPIView

from django.db.models import QuerySet

PERMISSION_ACTIONS_BY_METHOD = {"GET": "view", "POST": "add", "PUT": "change", "PATCH": "change", "DELETE": "delete"}


def check_api_user_permissions(view: GenericAPIView) -> bool:
    if view.request.user.is_superuser:
        return True

    queryset: QuerySet = view.get_queryset()
    app: str = queryset.model._meta.app_label
    model: str = queryset.model._meta.model_name
    action: str = PERMISSION_ACTIONS_BY_METHOD[view.request.method]

    permission: str = f"{app}.{action}_{model}"
    return permission in view.request.user.get_all_permissions()
