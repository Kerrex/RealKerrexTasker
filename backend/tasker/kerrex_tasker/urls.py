from django.conf.urls import url, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from kerrex_tasker.views import register, ProjectViewSet, PermissionViewSet, UserViewSet, CardViewSet, CategoryViewSet, \
    UserProjectPermissionViewSet, has_permission, PriorityViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('projects', ProjectViewSet)
router.register('permissions', PermissionViewSet)
router.register('users', UserViewSet)
router.register('cards', CardViewSet)
router.register('categories', CategoryViewSet)
router.register('user-project-permissions', UserProjectPermissionViewSet)
router.register('priorities', PriorityViewSet)

urlpatterns = [
    url(r'^api-auth-token/', obtain_auth_token),
    url(r'^api-register/', register),
    url(r'^api/', include(router.urls)),
    url(r'^api-has-permission/', has_permission)
]