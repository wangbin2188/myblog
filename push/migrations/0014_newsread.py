# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-23 02:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0013_headlinesfocus_headlinesicon_headlinessection'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsRead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('news_total', models.IntegerField()),
                ('important_news', models.IntegerField()),
                ('media_news', models.IntegerField()),
                ('yc_news', models.IntegerField()),
                ('album_news', models.IntegerField()),
                ('video_news', models.IntegerField()),
            ],
        ),
    ]
