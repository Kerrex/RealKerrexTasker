from django.conf.urls import url, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from kerrex_tasker.views import register, ProjectViewSet, PermissionViewSet, UserViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('projects', ProjectViewSet)
router.register('permissions', PermissionViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    url(r'^api-auth-token/', obtain_auth_token),
    url(r'^api-register/', register),
    url(r'^api/', include(router.urls))
]