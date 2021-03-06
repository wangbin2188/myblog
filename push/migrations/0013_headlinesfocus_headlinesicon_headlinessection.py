# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-16 08:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0012_communityrealtime'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeadLinesFocus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('focus1', models.IntegerField()),
                ('focus2', models.IntegerField()),
                ('focus3', models.IntegerField()),
                ('focus4', models.IntegerField()),
                ('focus5', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='HeadLinesIcon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('icon1', models.IntegerField()),
                ('icon2', models.IntegerField()),
                ('icon3', models.IntegerField()),
                ('icon4', models.IntegerField()),
                ('icon5', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='HeadLinesSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('yaowen', models.IntegerField()),
                ('shuoche', models.IntegerField()),
                ('photo', models.IntegerField()),
                ('shipin', models.IntegerField()),
                ('newcar', models.IntegerField()),
                ('pingce', models.IntegerField()),
                ('daogou', models.IntegerField()),
                ('diandong', models.IntegerField()),
                ('yongche', models.IntegerField()),
            ],
        ),
    ]
