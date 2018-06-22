from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from kerrex_tasker.models import Project, Card, Permission, Category


class CardViewTest(TestCase):
    def setUp(self):
        User.objects.create_user('someuser', 'test@test.pl', 'password').save()
        Permission(id=1, name='Permission', description='Permission').save()
        Permission(id=3, name='Read-only', description='Permission').save()
        Project(name='Project', default_permission_id=1, owner_id=1).save()
        Category(name='Category', order_in_project=0, project_id=1).save()
        Card(id=1, name='Card', category_id=1, order_in_category=0, created_by_id=1).save()
        self.client = APIClient()
        self.client.login(username='someuser', password='password')

    def test_successfully_update_card_no_order_change(self):
        request = '{"data":{"id":"1","attributes":{"name":"AfterUpdateCard","description":"",' \
                  '"order_in_category":0,"calendar_date_start":"Invalid date","calendar_date_end":"Invalid date",' \
                  '"show_on_calendar":false},"relationships":{"created_by":{"data":{"type":"Users","id":"1"}},' \
                  '"modified_by":{"data":{"type":"Users","id":"1"}},"priority":{"data":null},"category":{"data":{' \
                  '"type":"Categories","id":"1"}}},"type":"cards"}}'

        response = self.client.patch('/api/cards/1', request, content_type='application/vnd.api+json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Card.objects.first().name, 'AfterUpdateCard')

    def test_update_card_change_order_to_higher_in_same_category(self):
        Card(id=2, name='Card2', category_id=1, order_in_category=1, created_by_id=1).save()
        request = '{"data":{"id":"1","attributes":{"name":"Card","description":"",' \
                  '"order_in_category":1,"calendar_date_start":"Invalid date","calendar_date_end":"Invalid date",' \
                  '"show_on_calendar":false},"relationships":{"created_by":{"data":{"type":"Users","id":"1"}},' \
                  '"modified_by":{"data":{"type":"Users","id":"1"}},"priority":{"data":null},"category":{"data":{' \
                  '"type":"Categories","id":"1"}}},"type":"cards"}}'

        response = self.client.patch('/api/cards/1', request, content_type='application/vnd.api+json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Card.objects.get(pk=1).order_in_category, 1)
        self.assertEqual(Card.objects.get(pk=2).order_in_category, 0)

    def test_update_card_change_order_to_lower_in_same_category(self):
        card = Card.objects.first()
        card.order_in_category = 1
        card.save()
        Card(id=2, name='Card2', category_id=1, order_in_category=0, created_by_id=1).save()
        request = '{"data":{"id":"1","attributes":{"name":"Card","description":"",' \
                  '"order_in_category":0,"calendar_date_start":"Invalid date","calendar_date_end":"Invalid date",' \
                  '"show_on_calendar":false},"relationships":{"created_by":{"data":{"type":"Users","id":"1"}},' \
                  '"modified_by":{"data":{"type":"Users","id":"1"}},"priority":{"data":null},"category":{"data":{' \
                  '"type":"Categories","id":"1"}}},"type":"cards"}}'

        response = self.client.patch('/api/cards/1', request, content_type='application/vnd.api+json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Card.objects.get(pk=1).order_in_category, 0)
        self.assertEqual(Card.objects.get(pk=2).order_in_category, 1)

    def test_update_card_change_category(self):
        Card(id=2, name='Card2', category_id=1, order_in_category=1, created_by_id=1).save()
        Category(name='Category2', order_in_project=1, project_id=1).save()
        Card(id=3, name='Card3', category_id=2, order_in_category=1, created_by_id=1).save()
        request = '{"data":{"id":"3","attributes":{"name":"Card3","description":"",' \
                  '"order_in_category":1,"calendar_date_start":"Invalid date","calendar_date_end":"Invalid date",' \
                  '"show_on_calendar":false},"relationships":{"created_by":{"data":{"type":"Users","id":"1"}},' \
                  '"modified_by":{"data":{"type":"Users","id":"1"}},"priority":{"data":null},"category":{"data":{' \
                  '"type":"Categories","id":"1"}}},"type":"cards"}}'

        response = self.client.patch('/api/cards/3', request, content_type='application/vnd.api+json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Card.objects.get(pk=1).order_in_category, 0)
        self.assertEqual(Card.objects.get(pk=2).order_in_category, 2)
        self.assertEqual(Card.objects.get(pk=3).order_in_category, 1)
        self.assertEqual(len(Card.objects.filter(category_id=1)), 3)
        self.assertEqual(len(Card.objects.filter(category_id=2)), 0)

    def test_successfully_create_card(self):
        request = '{"data":{"attributes":{"name":"Nowa karta","description":"","date_created":null,' \
                  '"last_modified":null,"order_in_category":0,"calendar_date_start":"2017-10-30T21:48:31+01:00",' \
                  '"calendar_date_end":"2017-10-30T21:48:31+01:00","show_on_calendar":false},"relationships":{' \
                  '"created_by":{"data":null},"modified_by":{"data":null},"priority":{"data":null},"category":{' \
                  '"data":{"type":"Categories","id":"1"}}},"type":"cards"}}'

        response = self.client.post('/api/cards', request, content_type='application/vnd.api+json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Card.objects.all()), 2)

    def test_create_card_for_nonexistent_category(self):
        request = '{"data":{"attributes":{"name":"Nowa karta","description":"","date_created":null,' \
                  '"last_modified":null,"order_in_category":0,"calendar_date_start":"2017-10-30T21:48:31+01:00",' \
                  '"calendar_date_end":"2017-10-30T21:48:31+01:00","show_on_calendar":false},"relationships":{' \
                  '"created_by":{"data":null},"modified_by":{"data":null},"priority":{"data":null},"category":{' \
                  '"data":{"type":"Categories","id":"10"}}},"type":"cards"}}'

        response = self.client.post('/api/cards', request, content_type='application/vnd.api+json')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(Card.objects.all()), 1)

    def test_create_card_no_permission(self):
        project = Project.objects.get(pk=1)
        project.default_permission_id = 3
        project.save()

        User.objects.create_user('someotheruser', 'test2@test.pl', 'password').save()
        self.client.login(username='someotheruser', password='password')
        request = '{"data":{"attributes":{"name":"Nowa karta","description":"","date_created":null,' \
                  '"last_modified":null,"order_in_category":0,"calendar_date_start":"2017-10-30T21:48:31+01:00",' \
                  '"calendar_date_end":"2017-10-30T21:48:31+01:00","show_on_calendar":false},"relationships":{' \
                  '"created_by":{"data":null},"modified_by":{"data":null},"priority":{"data":null},"category":{' \
                  '"data":{"type":"Categories","id":"1"}}},"type":"cards"}}'

        response = self.client.post('/api/cards', request, content_type='application/vnd.api+json')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(Card.objects.all()), 1)