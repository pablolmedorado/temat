from django.contrib.auth import (
    authenticate,
    login as django_login,
    logout as django_logout,
)
from django.utils.datastructures import MultiValueDictKeyError

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    try:
        username = request.POST["username"]
        password = request.POST["password"]
    except MultiValueDictKeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if not user:
        return Response("Login failed. Invalid username or password.", status=status.HTTP_401_UNAUTHORIZED,)
    django_login(request._request, user)
    return Response()


@api_view(["POST"])
def logout(request):
    django_logout(request._request)
    return Response()
