import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from kerrex_tasker.models import Project, Category, Card, UserCardNotification
from kerrex_tasker.services.web_push_service import WebPushService


def create_unsaved_card_notification():
    some_user = User.objects.create_user('newuser', 'test@test.com', 'password')
    some_user.save()

    project = Project(name='project', default_permission_id=0, owner=some_user)
    project.save()

    category = Category(name='Card', order_in_project=0, project=project)
    category.save()

    new_card = Card(name='card', category=category, order_in_category=0)
    new_card.calendar_date_start = timezone.now() + datetime.timedelta(minutes=5)
    new_card.save()

    return UserCardNotification(user=some_user, card_id=1, minutes_before_start=10)


class WebPushServiceTestCase(TestCase):
    push_service = WebPushService()

    def test_is_eligible_when_is_eligible(self):
        card_notification = create_unsaved_card_notification()
        card_notification.save()

        result = self.push_service.is_eliglble_for_push(card_notification)

        self.assertTrue(result)

    def test_is_eligible_when_is_not_eligible(self):
        card_notification = create_unsaved_card_notification()
        card_notification.save()
        card = card_notification.card
        card.calendar_date_start = timezone.now() + datetime.timedelta(minutes=20)
        card.save()

        result = self.push_service.is_eliglble_for_push(card_notification)

        self.assertFalse(result)

    def test_is_eligible_when_date_is_in_past(self):
        card_notification = create_unsaved_card_notification()
        card_notification.save()
        card = card_notification.card
        card.calendar_date_start = timezone.now() - datetime.timedelta(minutes=50)
        card.save()

        result = self.push_service.is_eliglble_for_push(card_notification)

        self.assertTrue(result)

    def test_is_eligible_when_date_is_none(self):
        card_notification = create_unsaved_card_notification()
        card_notification.save()
        card = card_notification.card
        card.calendar_date_start = None
        card.save()

        result = self.push_service.is_eliglble_for_push(card_notification)

        self.assertFalse(result)
