# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-29 09:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0065_auto_20170929_1655'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=10)),
                ('version_dt', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
