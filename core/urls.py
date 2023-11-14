
from django.urls import path, include, re_path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    LogoutView
)

# DRF YASG imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# DRF YASG schema
schema_view = get_schema_view(
    openapi.Info(
        title="Djoser API",
        default_version="v1",
        description="""REST implementation of Django authentication system.
                        djoser library provides a set of Django Rest Framework views
                        to handle basic actions such as registration, login, logout,
                        """,
        contact=openapi.Contact(email="somecontactemail@mail.md"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # Add drf_yasg
    re_path(
        r"^api/v1/docs/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),

    path('api/auth/', include('djoser.urls')),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout')
]
