from rest_framework import routers

from .api.viewsets import EventTypeViewSet, EventViewSet

app_name = "events"

router = routers.DefaultRouter()
router.register(r"events", EventViewSet, basename="event")
router.register(r"event-types", EventTypeViewSet, basename="event-type")

urlpatterns = router.urls
