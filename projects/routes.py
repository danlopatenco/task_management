from rest_framework_nested import routers

from .views import ProjectViewSet


router = routers.DefaultRouter()
router.register(r'project', ProjectViewSet)


projects_router = routers.NestedSimpleRouter(router, r'project', lookup='project')
