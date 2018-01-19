import json

from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient

from kerrex_tasker.models import Project, UserProjectPermission, Permission


class ProjectViewSetTest(APITestCase):
    def setUp(self):
        self.create_three_users()
        self.client = APIClient()
        self.client.login(username='someuser1', password='password')

    def create_three_users(self):
        self.logged_user = User.objects.create_user('someuser1', 'test@test.pl', 'password')
        self.logged_user.save()
        User.objects.create_user('someuser2', 'test2@test.pl', 'password').save()
        User.objects.create_user('someuser3', 'test3@test.pl', 'password').save()

    def create_three_projects_not_available_for_logged_in_user(self):
        Project.objects.create(name='Project1', default_permission_id=1, owner_id=2).save()
        Project.objects.create(name='Project2', default_permission_id=1, owner_id=2).save()
        Project.objects.create(name='Project3', default_permission_id=1, owner_id=3).save()

    def create_three_projects_two_available_for_logged_in_user(self):
        Project(name='Project1', default_permission_id=1, owner_id=2).save()
        Project(name='Project2', default_permission_id=1, owner_id=2).save()
        Project(name='Project3', default_permission_id=1, owner_id=3).save()
        Permission(id=1, name='Permission', description='Permission').save()
        Permission(id=3, name='Permission2', description='Permission2').save()
        UserProjectPermission(permission_id=1, project_id=1, user_id=self.logged_user.id).save()
        UserProjectPermission(permission_id=3, project_id=2, user_id=self.logged_user.id).save()

    def create_three_projects_two_available_for_logged_in_user_and_owner(self):
        Project.objects.create(name='Project1', default_permission_id=1, owner_id=1).save()
        Project.objects.create(name='Project2', default_permission_id=1, owner_id=2).save()
        Project.objects.create(name='Project3', default_permission_id=1, owner_id=3).save()
        Permission(id=1, name='Permission', description='Permission').save()
        UserProjectPermission(permission_id=1, project_id=2, user_id=self.logged_user.id).save()

    def test_list_when_no_projects_available_for_user(self):
        self.create_three_projects_not_available_for_logged_in_user()

        response = self.client.get('/api/projects')

        self.assertEqual(response.data, [])

    def test_list_when_two_projects_available_for_user(self):
        self.create_three_projects_two_available_for_logged_in_user()

        response = self.client.get('/api/projects')

        self.assertEqual(len(response.data), 2)

    def test_list_when_two_projects_available_for_user_and_is_owner_of_one(self):
        self.create_three_projects_two_available_for_logged_in_user_and_owner()

        response = self.client.get('/api/projects')

        self.assertEqual(len(response.data), 2)

    def test_retrieve_when_project_not_exist(self):
        response = self.client.get('/api/projects/1')

        self.assertEqual(response.status_code, 404)

    def test_retrieve_when_project_exists_but_user_has_no_right(self):
        Project.objects.create(name='Project2', default_permission_id=2, owner_id=2).save()

        response = self.client.get('/api/projects/1')

        self.assertEqual(response.status_code, 404)

    def test_retrieve_when_project_exists_and_user_has_right(self):
        Permission(id=1, name='Permission', description='Permission').save()
        Permission(id=3, name='Permission2', description='Permission2').save()
        Project.objects.create(name='Project2', default_permission_id=1, owner_id=self.logged_user.id).save()

        response = self.client.get('/api/projects/1')

        self.assertEqual(response.status_code, 200)

    def test_add_new_project(self):
        Permission(id=1, name='Permission', description='Permission').save()
        request = '{"data":{"attributes":{"name":"hdfghdfg","description":"hdfghdfg","date_created":null,' \
                  '"last_modified":null},"relationships":{"default_permission":{"data":{"type":"Permissions",' \
                  '"id":"1"}},"owner":{"data":null}},"type":"projects"}} '

        response = self.client.post('/api/projects', request, content_type='application/vnd.api+json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Project.objects.all()), 1)

    def test_successfully_update_existing_project(self):
        Permission(id=1, name='Permission', description='Permission').save()
        Project.objects.create(name='Project2', default_permission_id=1, owner_id=self.logged_user.id).save()
        request = '{"data":{"id":"1","attributes":{"name":"New_name","description":"New_description",' \
                  '"date_created":"2017-09-24T16:43:56.057Z","last_modified":"2017-09-24T16:43:56.057Z"},' \
                  '"relationships":{"default_permission":{"data":{"type":"Permissions","id":"1"}},"owner":{"data":{' \
                  '"type":"Users","id":"1"}}},"type":"projects"}}'

        response = self.client.patch('/api/projects/1', request, content_type='application/vnd.api+json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.get(pk=1).name, 'New_name')

    def test_wrongly_update_existing_project(self):
        Permission(id=1, name='Permission', description='Permission').save()
        Project.objects.create(name='Project', default_permission_id=1, owner_id=self.logged_user.id).save()
        request = '{"data":{"id":"1","attributes":{"name":"aaaaaaaaaaaaaaaaaaaaaaaaaaaa","description":"New_description",' \
                  '"date_created":"2017-09-24T16:43:56.057Z","last_modified":"2017-09-24T16:43:56.057Z"},' \
                  '"relationships":{"default_permission":{"data":{"type":"Permissions","id":"1"}},"owner":{"data":{' \
                  '"type":"Users","id":"1"}}},"type":"projects"}}'

        response = self.client.patch('/api/projects/1', request, content_type='application/vnd.api+json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Project.objects.get(pk=1).name, 'Project')
