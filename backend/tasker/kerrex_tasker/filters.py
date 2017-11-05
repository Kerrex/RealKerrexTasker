from django.db.models import Q, QuerySet

from kerrex_tasker.models import Card


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


class CardFilter:
    CATEGORY_ID = 'filter[category_id]'
    CATEGORY_ID_MANY = 'filter[category_id][]'
    SHOW_ON_CALENDAR = 'filter[showOnCalendar]'
    CALENDAR_DATE_START = 'filter[calendarDateStart]'

    def __init__(self, queryset: QuerySet):
        self.queryset = queryset

    def filter(self, query_params):
        query = self.queryset
        if self.CATEGORY_ID in query_params:
            category_id = query_params[self.CATEGORY_ID]
            query = query.filter(category_id=category_id)

        # TODO Sprawdzić czy nowa metoda faktycznie działa
        if self.CATEGORY_ID_MANY in query_params:
            # category_ids = self.request.GET.getlist('filter[category_id][]')
            category_ids = query_params.getlist(self.CATEGORY_ID_MANY)
            query = query.filter(category_id__in=category_ids)

        if self.SHOW_ON_CALENDAR in query_params:
            show_on_calendar = query_params[self.SHOW_ON_CALENDAR] == 'true'
            query = query.filter(show_on_calendar=show_on_calendar)

        if self.CALENDAR_DATE_START in query_params:
            calendar_date_start = query_params[self.CALENDAR_DATE_START]
            query = query.filter(calendar_date_start=calendar_date_start if calendar_date_start != '' else None)

        return query


class UserCardPermissionFilter:
    PROJECT_ID = 'filter[project_id]'

    def __init__(self, queryset: QuerySet):
        self.queryset = queryset

    def filter(self, query_params):
        query = self.queryset
        if self.PROJECT_ID in query_params:
            project_id = query[self.PROJECT_ID]
            query = query.filter(project_id=project_id)

        return query
