# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-13 10:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kerrex_tasker', '0005_auto_20170810_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='calendar_date_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='card',
            name='calendar_date_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
