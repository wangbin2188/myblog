# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-08-24 02:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0050_customaccess'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customaccess',
            options={'permissions': (('app_active', 'visit app_active'), ('app_add', 'visit app_add'), ('app_retain', 'visit app_retain'), ('app_starts', 'visit app_starts'), ('app_channel', 'visit app_channel'), ('moduleuser', 'visit moduleuser'), ('app_stay', 'visit app_stay'), ('app_core', 'visit app_core'), ('app_core2', 'visit app_core2'), ('business', 'visit business'), ('app_business', 'visit app_business'), ('app_video', 'visit app_video'), ('app_media', 'visit app_media'), ('news_data', 'visit news_data'), ('posts_app', 'visit posts_app'), ('post_detail', 'visit post_detail'), ('car_coin', 'visit car_coin'))},
        ),
    ]
