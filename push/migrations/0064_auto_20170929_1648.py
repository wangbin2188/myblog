# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-29 08:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0063_auto_20170929_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='loglist',
            name='remark',
            field=models.CharField(max_length=40, null=True, verbose_name='\u5907\u6ce8'),
        ),
        migrations.AlterField(
            model_name='loglist',
            name='object_name',
            field=models.CharField(blank=True, max_length=20, verbose_name='name'),
        ),
    ]
