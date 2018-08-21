# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-28 04:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0059_auto_20170927_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='loglist',
            name='dt',
            field=models.BigIntegerField(blank=True, default=1480582478509, help_text='\u5fc5\u9700*', verbose_name='\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='loglist',
            name='tlsc',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u505c\u7559\u65f6\u957f'),
        ),
        migrations.AlterField(
            model_name='loglist',
            name='column_name',
            field=models.CharField(blank=True, max_length=20, verbose_name='\u680f\u76ee'),
        ),
        migrations.AlterField(
            model_name='loglist',
            name='object_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u5bf9\u8c61id'),
        ),
        migrations.AlterField(
            model_name='loglist',
            name='object_name',
            field=models.CharField(blank=True, max_length=20, verbose_name='\u5bf9\u8c61\u540d'),
        ),
        migrations.AlterField(
            model_name='loglist',
            name='page_name',
            field=models.ForeignKey(help_text='\u5fc5\u9700*', on_delete=django.db.models.deletion.CASCADE, to='push.PageSet', verbose_name='\u9875\u9762'),
        ),
        migrations.AlterField(
            model_name='loglist',
            name='section_name',
            field=models.CharField(blank=True, max_length=20, verbose_name='\u6bb5\u843d'),
        ),
        migrations.AlterField(
            model_name='loglist',
            name='type_desc',
            field=models.CharField(help_text='\u5fc5\u9700*', max_length=40, verbose_name='\u4e8b\u4ef6\u540d'),
        ),
        migrations.AlterField(
            model_name='loglist',
            name='type_name',
            field=models.ForeignKey(help_text='\u5fc5\u9700*', on_delete=django.db.models.deletion.CASCADE, to='push.TypeSet', verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='loglist',
            name='user_name',
            field=models.ForeignKey(default=2, help_text='\u5fc5\u9700*', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237\u540d'),
        ),
        migrations.AlterField(
            model_name='loglist',
            name='version',
            field=models.CharField(help_text='\u5fc5\u9700*', max_length=40, verbose_name='\u7248\u672c\u53f7'),
        ),
        migrations.AlterField(
            model_name='loglist',
            name='view_name',
            field=models.ForeignKey(help_text='\u5fc5\u9700*', on_delete=django.db.models.deletion.CASCADE, to='push.ViewSet', verbose_name='\u89c6\u56fe\u7c7b\u578b'),
        ),
    ]