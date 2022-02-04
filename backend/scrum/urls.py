from rest_framework_bulk.routes import BulkRouter

from .api.viewsets import (
    EffortViewSet,
    EpicViewSet,
    ProgressViewSet,
    SprintViewSet,
    TaskViewSet,
    UserStoryViewSet,
    UserStoryTypeViewSet,
)

app_name = "scrum"

router = BulkRouter()

router.register(r"effort", EffortViewSet, basename="effort")
router.register(r"user-stories/(?P<user_story>.+)/effort-log", EffortViewSet, basename="user-story-effort")

router.register(r"progress", ProgressViewSet, basename="progress")
router.register(r"user-stories/(?P<user_story>.+)/progress-log", ProgressViewSet, basename="user-story-progress")

router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"user-stories/(?P<user_story>.+)/tasks", TaskViewSet, basename="user-story-task")

router.register(r"user-stories", UserStoryViewSet, basename="user-story")
router.register(r"sprints/(?P<sprint>.+)/user-stories", UserStoryViewSet, basename="sprint-user-story")
router.register(r"epics/(?P<epic>.+)/user-stories", UserStoryViewSet, basename="epic-user-story")

router.register(r"sprints", SprintViewSet, basename="sprint")
router.register(r"epics", EpicViewSet, basename="epic")
router.register(r"user-story-types", UserStoryTypeViewSet, basename="user-story-type")

urlpatterns = router.urls
