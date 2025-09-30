"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.views import RedocViewBasicAuthentication, SwaggerViewBasicAuthentication

urlpatterns = [
    # admin path
    path("admin/", admin.site.urls),
    # doc paths
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/redoc/",
        RedocViewBasicAuthentication.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        "api/swagger/",
        SwaggerViewBasicAuthentication.as_view(url_name="schema"),
        name="swagger",
    ),
    # app paths
    path("resources/", include("resources.urls"), name="resources"),
    path("personnel/", include("personnel.urls"), name="personnel"),
    path("recruitment/", include("recruitment.urls"), name="recruitment"),
    path("salary/", include("salary.urls"), name="salary"),
    # jwt paths
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
