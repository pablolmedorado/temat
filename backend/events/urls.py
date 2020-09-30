from rest_framework import routers

from .views_api import EventApi, EventTypeApi

app_name = "events"

router = routers.DefaultRouter()
router.register(r"events", EventApi, basename="event")
router.register(r"event-types", EventTypeApi, basename="event-type")

urlpatterns = router.urls
