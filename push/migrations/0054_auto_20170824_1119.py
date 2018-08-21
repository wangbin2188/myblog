# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-08-24 03:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0053_auto_20170824_1100'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Access',
        ),
        migrations.AlterModelOptions(
            name='appindex',
            options={'permissions': (('app_active', 'Can visit app_active'), ('app_add', 'Can visit app_add'), ('app_retain', 'Can visit app_retain'), ('app_starts', 'Can visit app_starts'), ('app_channel', 'Can visit app_channel'), ('moduleuser', 'Can visit moduleuser'), ('app_stay', 'Can visit app_stay'), ('app_core', 'Can visit app_core'), ('app_core2', 'Can visit app_core2'), ('business', 'Can visit business'), ('app_business', 'Can visit app_business'), ('app_video', 'Can visit app_video'), ('app_media', 'Can visit app_media'), ('news_data', 'Can visit news_data'), ('posts_app', 'Can visit posts_app'), ('post_detail', 'Can visit post_dtail'), ('car_coin', 'Can visit car_coin'))},
        ),
    ]
