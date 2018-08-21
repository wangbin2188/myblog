# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-27 05:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0010_flow_operator_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flow',
            name='executor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='executor', to=settings.AUTH_USER_MODEL, verbose_name='\u6307\u6d3e\u7ed9'),
        ),
        migrations.AlterField(
            model_name='flow',
            name='executor_group',
            field=models.ManyToManyField(null=True, related_name='executor_group', to=settings.AUTH_USER_MODEL, verbose_name='\u5206\u914d\u7ed9'),
        ),
        migrations.AlterField(
            model_name='flow',
            name='remark',
            field=models.TextField(null=True, verbose_name='\u53d1\u8d77\u5185\u5bb9'),
        ),
        migrations.AlterField(
            model_name='flownode',
            name='executor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='operator_name', to=settings.AUTH_USER_MODEL, verbose_name='\u6307\u6d3e\u7ed9'),
        ),
        migrations.AlterField(
            model_name='flownode',
            name='remark',
            field=models.TextField(null=True, verbose_name='\u5907\u6ce8\u5185\u5bb9'),
        ),
    ]
