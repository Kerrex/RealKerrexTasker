class UserCardNotificationFilter:
    def __init__(self, queryset, user):
        self.queryset = queryset
        self.user = user

    def filter(self, query_params):
        if 'filter[card_id]' in query_params:
            card_id = query_params['filter[card_id]']
            query = self.queryset.filter(card_id=card_id, user=self.user)

        return query
