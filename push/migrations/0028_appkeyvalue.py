# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-06 07:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0027_business'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppKeyValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt', models.DateField()),
                ('c_key', models.CharField(max_length=20)),
                ('c_value', models.IntegerField()),
            ],
        ),
    ]
