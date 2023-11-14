from rest_framework_nested import routers

from .views import TaskViewSet


router = routers.DefaultRouter()
router.register(r'task', TaskViewSet)


projects_router = routers.NestedSimpleRouter(router, r'task', lookup='task')
