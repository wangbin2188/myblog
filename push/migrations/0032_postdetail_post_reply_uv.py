# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-19 05:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0031_appkey'),
    ]

    operations = [
        migrations.AddField(
            model_name='postdetail',
            name='post_reply_uv',
            field=models.IntegerField(default=0),
        ),
    ]
