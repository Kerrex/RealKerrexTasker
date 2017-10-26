from django.db.models import Q


class UserCardNotificationFilter:
    def __init__(self, queryset, user):
        self.queryset = queryset
        self.user = user

    def filter(self, query_params):
        query = self.queryset
        if 'filter[card_id]' in query_params:
            card_id = query_params['filter[card_id]']
            query = query.filter(card_id=card_id, user=self.user)

        return query.all()


class UserFilter:
    USERNAME_OR_EMAIL = 'filter[usernameOrEmail]'

    def __init__(self, queryset):
        self.queryset = queryset

    def filter(self, query_params):
        query = self.queryset
        if self.USERNAME_OR_EMAIL in query_params:
            username_or_email = query_params[self.USERNAME_OR_EMAIL]
            query = query.filter(Q(username=username_or_email) | Q(email=username_or_email))

        return query.all()


class CategoryFilter:
    PROJECT_ID = 'filter[project_id]'

    def __init__(self, queryset):
        self.queryset = queryset

    def filter(self, query_params):
        query = self.queryset
        if self.PROJECT_ID in query_params:
            project_id = query_params['filter[project_id]']
            query = query.filter(project=project_id)

        return query