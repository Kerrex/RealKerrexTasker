from django.db import models


class CardNotificationManager(models.Manager):
    def get_card_name(self):
        return