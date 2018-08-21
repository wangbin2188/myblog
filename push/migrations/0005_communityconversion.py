# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-28 07:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0004_auto_20161025_0734'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunityConversion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('community_tab', models.IntegerField()),
                ('posts_entry', models.IntegerField()),
                ('specific_posts_entry', models.IntegerField()),
                ('posts_publish', models.IntegerField()),
                ('week', models.CharField(max_length=20)),
                ('month', models.CharField(max_length=20)),
                ('date', models.DateField()),
            ],
        ),
    ]