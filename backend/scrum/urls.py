from rest_framework import routers

from .views_api import EffortApi, EpicApi, ProgressApi, SprintApi, TaskApi, UserStoryApi, UserStoryTypeApi

app_name = "scrum"

router = routers.DefaultRouter()

router.register(r"effort", EffortApi, basename="effort")
router.register(r"user-stories/(?P<user_story>.+)/effort-log", EffortApi, basename="user-story-effort")

router.register(r"progress", ProgressApi, basename="progress")
router.register(r"user-stories/(?P<user_story>.+)/progress-log", ProgressApi, basename="user-story-progress")

router.register(r"tasks", TaskApi, basename="task")
router.register(r"user-stories/(?P<user_story>.+)/tasks", TaskApi, basename="user-story-task")

router.register(r"user-stories", UserStoryApi, basename="user-story")
router.register(r"sprints/(?P<sprint>.+)/user-stories", UserStoryApi, basename="sprint-user-story")
router.register(r"epics/(?P<epic>.+)/user-stories", UserStoryApi, basename="epic-user-story")

router.register(r"sprints", SprintApi, basename="sprint")
router.register(r"epics", EpicApi, basename="epic")
router.register(r"user-story-types", UserStoryTypeApi, basename="user-story-type")

urlpatterns = router.urls
