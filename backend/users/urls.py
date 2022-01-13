from django.urls import path

from rest_framework import routers

from .api.viewsets import GroupViewSet, UserViewSet
from .api.views import login, logout

app_name = "users"

router = routers.DefaultRouter()
router.register(r"groups", GroupViewSet, basename="group")
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
]

urlpatterns = urlpatterns + router.urls
