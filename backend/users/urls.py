from rest_framework import routers

from django.urls import path

from .api.views import login, logout
from .api.viewsets import GroupViewSet, UserViewSet

app_name = "users"

router = routers.DefaultRouter()
router.register(r"groups", GroupViewSet, basename="group")
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
]

urlpatterns = urlpatterns + router.urls
