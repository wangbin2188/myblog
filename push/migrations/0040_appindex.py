# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-27 01:59
from __future__ import unicode_literals

from django.db import migrations, models
import push.models


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0039_auto_20170726_1817'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt', models.DateField()),
                ('c_key', models.CharField(max_length=30)),
                ('c_value', push.models.JSONField()),
            ],
        ),
    ]
