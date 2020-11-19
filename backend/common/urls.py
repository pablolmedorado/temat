from rest_framework_bulk.routes import BulkRouter

from .api.viewsets import NotificationViewSet, TagViewSet

app_name = "common"

router = BulkRouter()
router.register(r"notifications", NotificationViewSet, basename="notification")
router.register(r"tags", TagViewSet, basename="tag")

urlpatterns = router.urls
