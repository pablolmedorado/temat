from django.urls import path

from rest_framework import routers

from .views import login, logout
from .views_api import GroupApi, UserApi

app_name = "users"

router = routers.DefaultRouter()
router.register(r"groups", GroupApi, basename="group")
router.register(r"users", UserApi, basename="user")

urlpatterns = [
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
]

urlpatterns = urlpatterns + router.urls
