# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-24 06:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0005_auto_20171023_1814'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flow',
            name='c_dt',
        ),
        migrations.AddField(
            model_name='flow',
            name='create_dt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='\u521b\u5efa\u65f6\u95f4'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='flow',
            name='end_dt',
            field=models.DateField(blank=True, null=True, verbose_name='\u4efb\u52a1\u5b8c\u6210'),
        ),
        migrations.AddField(
            model_name='flow',
            name='start_dt',
            field=models.DateField(blank=True, null=True, verbose_name='\u4efb\u52a1\u5f00\u59cb'),
        ),
        migrations.AddField(
            model_name='flow',
            name='update_dt',
            field=models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4'),
        ),
    ]
