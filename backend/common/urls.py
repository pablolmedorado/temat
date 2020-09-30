from rest_framework_bulk.routes import BulkRouter

from .views_api import NotificationApi, TagApi

app_name = "common"

router = BulkRouter()
router.register(r"notifications", NotificationApi, basename="notification")
router.register(r"tags", TagApi, basename="tag")

urlpatterns = router.urls
