# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-26 09:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0037_auto_20170726_1617'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appbasic',
            old_name='date',
            new_name='dt',
        ),
    ]