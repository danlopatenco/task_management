from rest_framework_nested import routers

from .views import TimeEntryViewSet, TimeTrackerViewSet


router = routers.DefaultRouter()

router.register(r'time-entries', TimeEntryViewSet)
router.register(r'time-trackers', TimeTrackerViewSet)
