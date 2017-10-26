from django.contrib.auth.models import User
from django.test import TestCase

from kerrex_tasker.filters import UserCardNotificationFilter
from kerrex_tasker.models import UserCardNotification


class UserCardNotificationFilterTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('username', 'user@user.pl', 'password')
        query = UserCardNotification.objects
        self.filter = UserCardNotificationFilter(query, self.user)

    def test_filter_non_empty_params(self):
        notification = UserCardNotification(user=self.user, card_id=1, minutes_before_start=10)
        notification2 = UserCardNotification(user=self.user, card_id=2, minutes_before_start=10)
        notification3 = UserCardNotification(user=self.user, card_id=1, minutes_before_start=10)
        notification.save()
        notification2.save()
        notification3.save()
        query_params = {'filter[card_id]': 1}

        filtered_query = self.filter.filter(query_params)

        self.assertEqual(len(filtered_query), 2)

    def test_filter_empty_params(self):
        notification = UserCardNotification(user=self.user, card_id=1, minutes_before_start=10)
        notification2 = UserCardNotification(user=self.user, card_id=2, minutes_before_start=10)
        notification3 = UserCardNotification(user=self.user, card_id=1, minutes_before_start=10)
        notification.save()
        notification2.save()
        notification3.save()
        query_params = {}

        filtered_query = self.filter.filter(query_params)

        self.assertEqual(len(filtered_query), 3)
