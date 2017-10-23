import datetime
import json
from django.utils import timezone

from pywebpush import webpush, WebPushException

from tasker import settings

CLAIMS = {"sub": "mailto:romen3@gmail.com"}
PRIVATE_KEY = settings.WEBPUSH_PRIVATE_KEY
MESSAGE_STRING = '{} starts in {} minutes!'


class WebPushService:
    def send_push(self, subscription_id, card_notification):
        subscription_data = json.loads(subscription_id)
        data_to_send = MESSAGE_STRING.format(card_notification.get_card_name(), card_notification.minutes_before_start)

        try:
            webpush(subscription_data, data_to_send, vapid_private_key=PRIVATE_KEY, vapid_claims=CLAIMS)
            return True
        except WebPushException:
            print("Endpoint not registered! Removing")
            return False

    def is_eliglble_for_push(self, card_notification):
        now = timezone.now()
        card = card_notification.card
        date_start = card.calendar_date_start
        minutes_before_start = datetime.timedelta(minutes=card_notification.minutes_before_start)

        is_eliglble = date_start is not None and ((now + minutes_before_start) > card.calendar_date_start
                                                  or card.calendar_date_start < now)

        return is_eliglble
