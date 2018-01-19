import datetime
from unittest.mock import MagicMock

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.utils import timezone

from kerrex_tasker.models import UserCardNotification, Card, Project, Category, UserNotification
from kerrex_tasker.views import NotifyView


def create_three_users():
    for i in range(1, 3):
        new_user = User.objects.create_user('user{}'.format(i), 'email{}@test.pl'.format(i), 'somepassword')
        new_user.save()


def create_three_cards():
    some_user = User.objects.create_user('newuser', 'test@test.com', 'password')
    some_user.save()
    project = Project(name='project', default_permission_id=0, owner=some_user)
    project.save()
    category = Category(name='Card', order_in_project=0, project=project)
    category.save()
    for i in range(1, 3):
        new_card = Card(name='card{}'.format(i), category=category, order_in_category=0)
        new_card.calendar_date_start = timezone.now() - datetime.timedelta(minutes=5)
        new_card.save()


class NotifyTestCase(TestCase):
    client = Client()

    def test_notify_when_card_notifications_are_eligible_for_push(self):
        # given
        create_three_users()
        NotifyView.push_service.send_push = MagicMock(return_value=True)
        NotifyView.push_service.is_eliglble_for_push = MagicMock(return_value=True)
        user = User.objects.create_user('newuser2', 'test2@test.com', 'password')

        user_device = UserNotification(user=user, subscription_id='aaaaa')
        user_device.save()

        card_notification1 = UserCardNotification(user=user, card_id=1, minutes_before_start=10)
        card_notification2 = UserCardNotification(user=user, card_id=2, minutes_before_start=10)
        card_notification3 = UserCardNotification(user=user, card_id=3, minutes_before_start=10)

        card_notification1.save()
        card_notification2.save()
        card_notification3.save()

        # when
        self.client.post('/api-notify/', data='  ', content_type='application/json')

        # then
        card_notifications = UserCardNotification.objects.all()
        user_devices = UserNotification.objects.all()
        self.assertEqual(len(card_notifications), 0)
        self.assertEqual(len(user_devices), 1)

    def test_notify_when_one_card_notification_is_eligible_for_push(self):
        # given
        create_three_users()
        NotifyView.push_service.send_push = MagicMock(return_value=True)
        user = User.objects.create_user('newuser2', 'test2@test.com', 'password')

        user_device = UserNotification(user=user, subscription_id='aaaaa')
        user_device.save()

        card_notification1 = UserCardNotification(user=user, card_id=1, minutes_before_start=10)
        card_notification2 = UserCardNotification(user=user, card_id=2, minutes_before_start=10)
        card_notification3 = UserCardNotification(user=user, card_id=3, minutes_before_start=10)
        NotifyView.push_service.is_eliglble_for_push = \
            MagicMock(side_effect=lambda x: {card_notification1: True}.get(x, False))

        card_notification1.save()
        card_notification2.save()
        card_notification3.save()

        # when
        self.client.post('/api-notify/', data='  ', content_type='application/json')

        # then
        card_notifications = UserCardNotification.objects.all()
        user_devices = UserNotification.objects.all()
        self.assertEqual(len(card_notifications), 2)
        self.assertEqual(len(user_devices), 1)

    def test_notify_when_eligible_for_push_but_device_incorrect(self):
        # given
        create_three_users()
        NotifyView.push_service.send_push = MagicMock(return_value=False)
        NotifyView.push_service.is_eliglble_for_push = MagicMock(return_value=True)
        user = User.objects.create_user('newuser2', 'test2@test.com', 'password')

        user_device = UserNotification(user=user, subscription_id='aaaaa')
        user_device.save()

        card_notification1 = UserCardNotification(user=user, card_id=1, minutes_before_start=10)
        card_notification2 = UserCardNotification(user=user, card_id=2, minutes_before_start=10)
        card_notification3 = UserCardNotification(user=user, card_id=3, minutes_before_start=10)

        card_notification1.save()
        card_notification2.save()
        card_notification3.save()

        # when
        self.client.post('/api-notify/', data='  ', content_type='application/json')

        # then
        card_notifications = UserCardNotification.objects.all()
        user_devices = UserNotification.objects.all()
        self.assertEqual(len(card_notifications), 0)
        self.assertEqual(len(user_devices), 0)
