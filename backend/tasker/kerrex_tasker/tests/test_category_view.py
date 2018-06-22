from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from kerrex_tasker.models import Project, Permission, Category


class CategoryViewTest(TestCase):
    def setUp(self):
        User.objects.create_user('someuser', 'test@test.pl', 'password').save()
        Permission(id=1, name='Permission', description='Permission').save()
        Project(name='Project', default_permission_id=1, owner_id=1).save()
        self.client = APIClient()
        self.client.login(username='someuser', password='password')

    def test_correct_data_should_create_category(self):
        request = '{"data":{"attributes":{"name":"NewCategory","order_in_project":null},"relationships":{"project":{' \
                  '"data":{"type":"Projects","id":"1"}}},"type":"categories"}} '

        response = self.client.post('/api/categories', request, content_type='application/vnd.api+json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Category.objects.all()), 1)

    def test_incorrect_data_should_not_create_category(self):
        request = '{"data":{"attributes":{"name":"NewCategory","order_in_project":null},"relationships":{"project":{' \
                  '"data":{"type":"Projects","id":"10"}}},"type":"categories"}} '

        response = self.client.post('/api/categories', request, content_type='application/vnd.api+json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(Category.objects.all()), 0)