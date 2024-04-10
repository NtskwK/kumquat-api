"""
URL configuration for kumquatAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

import kmqtAuth.views
import program.views

user_router = routers.DefaultRouter()
user_router.register("info", kmqtAuth.views.KmqtUserInfoViewSet)
user_router.register("users/create", kmqtAuth.views.CreateKmqtUserViewSet)
user_router.register("users", kmqtAuth.views.KmqtUserViewSet)

program_router = routers.DefaultRouter()
program_router.register("programs", program.views.ProgramViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/", include(user_router.urls)),
    path("api/", include(program_router.urls)),

    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
