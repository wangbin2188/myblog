# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-30 01:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0067_auto_20170929_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loglist',
            name='page_name',
            field=models.ForeignKey(help_text='\u7528\u6237\u884c\u4e3a\u6240\u5728\u9875\u9762\uff0c\u5fc5\u9700*', on_delete=django.db.models.deletion.CASCADE, to='push.PageSet', verbose_name='\u9875\u9762'),
        ),
    ]
