# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-26 08:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0035_auto_20170726_1121'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppBasic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('c_key', models.CharField(max_length=20)),
                ('c_value', models.IntegerField()),
                ('platform', models.CharField(max_length=20)),
            ],
        ),
    ]
