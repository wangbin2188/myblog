# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-19 09:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flow',
            name='executor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='executor', to=settings.AUTH_USER_MODEL, verbose_name='\u987a\u4f4d\u6267\u884c\u8005'),
        ),
        migrations.AlterField(
            model_name='flow',
            name='initiator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partner_name', to=settings.AUTH_USER_MODEL, verbose_name='\u53d1\u8d77\u4eba'),
        ),
        migrations.AlterField(
            model_name='flownode',
            name='executor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='operator_name', to=settings.AUTH_USER_MODEL, verbose_name='\u987a\u4f4d\u6267\u884c\u8005'),
        ),
        migrations.AlterField(
            model_name='flownode',
            name='operator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operator', to=settings.AUTH_USER_MODEL, verbose_name='\u64cd\u4f5c\u8005'),
        ),
    ]
