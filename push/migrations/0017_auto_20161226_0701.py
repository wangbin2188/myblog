# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-26 07:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0016_newsdata_news_read'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newsdata',
            old_name='news_commment',
            new_name='news_comment',
        ),
    ]
