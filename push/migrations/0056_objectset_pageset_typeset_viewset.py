# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-26 09:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0055_appchart_chart_column'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_name', models.CharField(max_length=20)),
                ('object_desc', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PageSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_name', models.CharField(max_length=20)),
                ('page_name', models.CharField(max_length=40)),
                ('page_desc', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='TypeSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=20)),
                ('type_desc', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ViewSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view_name', models.CharField(max_length=20)),
                ('view_desc', models.CharField(max_length=20)),
            ],
        ),
    ]