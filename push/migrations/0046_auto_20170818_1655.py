# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-08-18 08:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0045_appchart'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AppCar',
        ),
        migrations.DeleteModel(
            name='AppKeyValue',
        ),
    ]
