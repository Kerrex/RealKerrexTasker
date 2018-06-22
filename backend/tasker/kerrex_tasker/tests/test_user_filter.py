from django.contrib.auth.models import User
from django.test import TestCase

from kerrex_tasker.filters import UserFilter


class UserFilterTest(TestCase):
    def setUp(self):
        query = User.objects
        self.filter = UserFilter(query)

    def test_filter_by_username(self):
        user = User.objects.create_user('username', 'test@test.pl', 'password')
        user2 = User.objects.create_user('username2', 'test2@test.pl', 'password')
        user.save()
        user2.save()

        query_params = {UserFilter.USERNAME_OR_EMAIL: 'username'}

        filtered_query = self.filter.filter(query_params)

        self.assertEqual(filtered_query.first(), user)
        self.assertEqual(len(filtered_query), 1)

    def test_filter_by_email(self):
        user = User.objects.create_user('username', 'test@test.pl', 'password')
        user2 = User.objects.create_user('username2', 'test2@test.pl', 'password')
        user.save()
        user2.save()

        query_params = {UserFilter.USERNAME_OR_EMAIL: 'test2@test.pl'}

        filtered_query = self.filter.filter(query_params)

        self.assertEqual(filtered_query.first(), user2)
        self.assertEqual(len(filtered_query), 1)

    def test_filter_no_found(self):
        user = User.objects.create_user('username', 'test@test.pl', 'password')
        user2 = User.objects.create_user('username2', 'test2@test.pl', 'password')
        user.save()
        user2.save()

        query_params = {UserFilter.USERNAME_OR_EMAIL: 'nothingfound'}

        filtered_query = self.filter.filter(query_params)

        self.assertEqual(len(filtered_query), 0)