# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-08-30 03:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0054_auto_20170824_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='appchart',
            name='chart_column',
            field=models.CharField(default='summary', max_length=20),
        ),
    ]
