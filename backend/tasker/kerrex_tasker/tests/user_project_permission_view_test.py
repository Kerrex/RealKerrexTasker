from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from kerrex_tasker.models import Card, UserCardNotification, Project, UserProjectPermission, Permission


class UserProjectPermissionViewTest(TestCase):
    def setUp(self):
        self.create_three_users()
        self.client = APIClient()
        Permission(id=1, name="Default permission", description='Default permission').save()

    def create_three_users(self):
        self.logged_user = User.objects.create_user('someuser1', 'test@test.pl', 'password')
        self.logged_user.save()
        User.objects.create_user('someuser2', 'test2@test.pl', 'password').save()
        User.objects.create_user('someuser3', 'test3@test.pl', 'password').save()

    def test_add_project_permission(self):
        Project(name='Project', default_permission_id=1, owner_id=self.logged_user.id).save()
        self.client.login(username='someuser1', password='password')

        request = '{"data":{"relationships":{"given_by":{"data":null},"permission":{"data":null},"project":{"data":{' \
                  '"type":"Projects","id":"1"}},"user":{"data":{"type":"Users","id":"2"}}},' \
                  '"type":"userProjectPermissions"}}'

        response = self.client.post('/api/user-project-permissions', request, content_type='application/vnd.api+json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(UserProjectPermission.objects.all()), 1)
        self.assertEqual(UserProjectPermission.objects.first().given_by_id, self.logged_user.id)

    def test_add_project_has_no_permission_to_edit(self):
        Project(name='Project', default_permission_id=2, owner_id=self.logged_user.id).save()
        self.client.logout()
        self.client.login(username='someuser3', password='password')
        request = '{"data":{"relationships":{"given_by":{"data":null},"permission":{"data":null},"project":{"data":{' \
                  '"type":"Projects","id":"1"}},"user":{"data":{"type":"Users","id":"1"}}},' \
                  '"type":"userProjectPermissions"}}'

        response = self.client.post('/api/user-project-permissions', request, content_type='application/vnd.api+json')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(UserProjectPermission.objects.all()), 0)

    def test_edit_user_project_permission(self):
        Project(name='Project', default_permission_id=1, owner_id=self.logged_user.id).save()
        self.client.login(username='someuser1', password='password')
        Permission(id=2, name="Other permission", description='Other permission').save()
        UserProjectPermission(id=1, given_by=self.logged_user, permission_id=1, project_id=1, user_id=2).save()
        request = '{"data":{"id":"1","relationships":{"given_by":{"data":{"type":"Users","id":"1"}},"permission":{' \
                  '"data":{"type":"Permissions","id":"2"}},"project":{"data":{"type":"Projects","id":"1"}},' \
                  '"user":{"data":{"type":"Users","id":"2"}}},"type":"userProjectPermissions"}} '

        response = self.client.patch('/api/user-project-permissions/1', request,
                                     content_type='application/vnd.api+json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(UserProjectPermission.objects.all()), 1)
        self.assertEqual(UserProjectPermission.objects.first().permission_id, 2)

    def test_edit_user_project_permission_no_permission_to_edit(self):
        Project(name='Project', default_permission_id=2, owner_id=self.logged_user.id).save()
        self.client.logout()
        self.client.login(username='someuser3', password='password')
        Permission(id=2, name="Other permission", description='Other permission').save()
        UserProjectPermission(id=1, given_by=self.logged_user, permission_id=1, project_id=1, user_id=2).save()
        request = '{"data":{"id":"1","relationships":{"given_by":{"data":{"type":"Users","id":"1"}},"permission":{' \
                  '"data":{"type":"Permissions","id":"2"}},"project":{"data":{"type":"Projects","id":"1"}},' \
                  '"user":{"data":{"type":"Users","id":"2"}}},"type":"userProjectPermissions"}} '

        response = self.client.patch('/api/user-project-permissions/1', request,
                                     content_type='application/vnd.api+json')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(UserProjectPermission.objects.all()), 1)
        self.assertEqual(UserProjectPermission.objects.first().permission_id, 1)
