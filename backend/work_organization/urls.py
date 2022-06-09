from rest_framework_bulk.routes import BulkRouter

from .api.viewsets import GreenWorkingDayViewSet, HolidayTypeViewSet, HolidayViewSet, SupportWorkingDayViewSet

app_name = "work_organization"

router = BulkRouter()
router.register(r"holidays", HolidayViewSet, basename="holiday")
router.register(r"holiday-types", HolidayTypeViewSet, basename="holiday-type")
router.register(r"green-days", GreenWorkingDayViewSet, basename="green-day")
router.register(r"support", SupportWorkingDayViewSet, basename="support")

urlpatterns = router.urls
