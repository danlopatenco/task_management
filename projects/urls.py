from django.urls import path, include

from .routes import router

urlpatterns = [
    path('', include(router.urls), name='projects_api')
]
