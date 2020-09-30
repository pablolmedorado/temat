from rest_framework_bulk.routes import BulkRouter

from .views_api import GreenWorkingDayApi, HolidayApi, HolidayTypeApi, SupportWorkingDayApi

app_name = "work_organization"

router = BulkRouter()
router.register(r"holidays", HolidayApi, basename="holiday")
router.register(r"holiday-types", HolidayTypeApi, basename="holiday-type")
router.register(r"green-days", GreenWorkingDayApi, basename="green-day")
router.register(r"support", SupportWorkingDayApi, basename="support")

urlpatterns = router.urls
