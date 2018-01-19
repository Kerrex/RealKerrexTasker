from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from kerrex_tasker.models import Card, UserCardNotification


class UserCardNotificationViewTest(TestCase):
    def setUp(self):
        self.create_three_users()
        self.client = APIClient()

    def create_three_users(self):
        self.logged_user = User.objects.create_user('someuser1', 'test@test.pl', 'password')
        self.logged_user.save()
        User.objects.create_user('someuser2', 'test2@test.pl', 'password').save()
        User.objects.create_user('someuser3', 'test3@test.pl', 'password').save()

    def test_add_new_notification(self):
        self.client.login(username='someuser1', password='password')
        Card(name='card', category_id=1, order_in_category=0).save()
        request = '{"data":{"attributes":{"minutes_before_start":10},"relationships":{"user":{"data":null},' \
                  '"card":{"data":{"type":"Cards","id":"1"}}},"type":"userCardNotifications"}}'

        response = self.client.post('/api/user-card-notifications', request, content_type='application/vnd.api+json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(UserCardNotification.objects.all()), 1)

    def test_add_new_notification_not_logged_in(self):
        Card(name='card', category_id=1, order_in_category=0).save()
        request = '{"data":{"attributes":{"minutes_before_start":10},"relationships":{"user":{"data":null},' \
                  '"card":{"data":{"type":"Cards","id":"1"}}},"type":"userCardNotifications"}}'

        response = self.client.post('/api/user-card-notifications', request, content_type='application/vnd.api+json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(UserCardNotification.objects.all()), 0)

    def test_add_new_notification_wrong_card(self):
        self.client.login(username='someuser1', password='password')
        Card(name='card', category_id=1, order_in_category=0).save()
        request = '{"data":{"attributes":{"minutes_before_start":10},"relationships":{"user":{"data":null},' \
                  '"card":{"data":{"type":"Cards","id":"100"}}},"type":"userCardNotifications"}}'

        response = self.client.post('/api/user-card-notifications', request, content_type='application/vnd.api+json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(UserCardNotification.objects.all()), 0)
