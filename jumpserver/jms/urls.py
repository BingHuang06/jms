"""jms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

import rest_framework
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

route = DefaultRouter()

from users.router import user_router
from assets.router import asset_router
from perms.router import perm_router
from utils.router import util_router

route.registry.extend(user_router.registry)
route.registry.extend(asset_router.registry)
route.registry.extend(perm_router.registry)
route.registry.extend(util_router.registry)

urlpatterns = [
    path('', include(route.urls)),
    path('docs/', include_docs_urls("跳板机平台API文档")),
    path('api-auth/', include("rest_framework.urls")),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
]
