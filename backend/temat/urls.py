"""backend URL Configuration

The `urlpatterns` list routes URLs to views. Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django_js_reverse import views as js_reverse

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from common.views import ClientSPA

urlpatterns = [
    path("", ClientSPA.as_view(), name="app"),
    path("", include("pwa.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("js-reverse", js_reverse.urls_js, name="js_reverse"),
    path("admin/", admin.site.urls),
    path("api/common/", include("common.urls", "common")),
    path("api/users/", include("users.urls", "users")),
    path("api/calendar/", include("events.urls", "calendar")),
    path("api/work-organization/", include("work_organization.urls", "work-organization")),
    path("api/scrum/", include("scrum.urls", "scrum")),
    path("api/breakfasts/", include("breakfasts.urls", "breakfasts")),
]

if "hijack" in settings.INSTALLED_APPS:
    from hijack import urls as hijack_urls

    urlpatterns += [path("hijack/", include(hijack_urls))]

if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
