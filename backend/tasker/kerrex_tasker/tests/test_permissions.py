from django.contrib.auth.models import User
from django.test import TestCase

from kerrex_tasker.models import Project, UserProjectPermission
from kerrex_tasker.permissions import has_permissions


def create_new_project(owner):
    new_project = Project()
    new_project.default_permission_id = 1
    new_project.name = 'Some project name'
    new_project.description = 'Some project description'
    new_project.owner = owner
    new_project.save()
    return new_project


class PermissionTestCase(TestCase):
    def test_has_permission_if_is_owner(self):
        """has_permission should return true if user is owner of project"""
        user = User.objects.create_user('newuser', 'test@test.com', 'password')
        user.save()
        new_project = create_new_project(user)

        has_perm = has_permissions(new_project.id, user)

        self.assertTrue(has_perm)

    def test_has_permission_if_not_owner_and_not_permission_not_default(self):
        """has_permission should return false if user is not owner, has no perm and is not allowed by default"""
        owner = User.objects.create_user('owner', 'owner@owner.com', 'password')
        owner.save()
        user = User.objects.create_user('someuser', 'test@test.com', 'password')
        user.save()
        project = create_new_project(owner)
        project.default_permission_id = 2
        project.save()

        has_perm = has_permissions(project.id, user)

        self.assertFalse(has_perm)

    def test_has_permission_if_not_owner_and_has_permission_not_default(self):
        """has_permission should return true if user is not owner and has permission for project"""
        owner = User.objects.create_user('owner', 'owner@owner.com', 'password')
        owner.save()
        user = User.objects.create_user('someuser', 'test@test.com', 'password')
        user.save()
        project = create_new_project(owner)
        project.default_permission_id = 2
        project.save()
        permission = UserProjectPermission(project=project, user=user, permission_id=1)
        permission.save()

        has_perm = has_permissions(project.id, user)

        self.assertTrue(has_perm)

    def test_has_permission_if_not_owner_and_blocked(self):
        """has_permission should return false is user is not owner and is blocked"""
        owner = User.objects.create_user('owner', 'owner@owner.com', 'password')
        owner.save()
        user = User.objects.create_user('someuser', 'test@test.com', 'password')
        user.save()
        project = create_new_project(owner)
        permission = UserProjectPermission(project=project, user=user, permission_id=4)
        permission.save()

        has_perm = has_permissions(project.id, user)

        self.assertFalse(has_perm)

    def test_has_permission_if_not_owner_no_permission_allowed_by_default(self):
        """has_permission should return true if user is not owner, has no permission but is allowed by default"""
        owner = User.objects.create_user('owner', 'owner@owner.com', 'password')
        owner.save()
        user = User.objects.create_user('someuser', 'test@test.com', 'password')
        user.save()
        project = create_new_project(owner)

        has_perm = has_permissions(project.id, user)

        self.assertTrue(has_perm)

    def test_has_permission_if_owner_and_blocked(self):
        """has_permission should return true if user is blocked but is owner of the project"""
        owner = User.objects.create_user('owner', 'owner@owner.com', 'password')
        owner.save()
        project = create_new_project(owner)
        permission = UserProjectPermission(project=project, user=owner, permission_id=4)
        permission.save()

        has_perm = has_permissions(project.id, owner)

        self.assertTrue(has_perm)
