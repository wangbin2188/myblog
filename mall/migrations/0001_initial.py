# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-11-06 09:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_c', models.CharField(max_length=20, verbose_name='\u4e00\u7ea7\u5206\u7c7b')),
                ('second_c', models.CharField(max_length=20, verbose_name='\u4e8c\u7ea7\u5206\u7c7b')),
                ('three_c', models.CharField(max_length=20, verbose_name='\u4e09\u7ea7\u5206\u7c7b')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('receiver', models.CharField(max_length=20, verbose_name='\u6536\u8d27\u4eba')),
                ('receiver_phone', models.IntegerField(verbose_name='\u6536\u8d27\u624b\u673a\u53f7')),
                ('receiver_address', models.TextField(verbose_name='\u6536\u8d27\u5730\u5740')),
                ('amount', models.IntegerField(verbose_name='\u8ba2\u5355\u603b\u4ef7')),
                ('order_status', models.IntegerField(verbose_name='\u8ba2\u5355\u72b6\u6001')),
                ('logistics', models.IntegerField(null=True, verbose_name='\u8fd0\u5355\u53f7')),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consumer_user', to=settings.AUTH_USER_MODEL, verbose_name='\u8d2d\u4e70\u4eba')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=20, verbose_name='\u54c1\u724c')),
                ('product_name', models.CharField(max_length=40, verbose_name='\u5546\u54c1\u540d\u79f0')),
                ('product_price', models.IntegerField(verbose_name='\u4ef7\u683c')),
                ('product_desc', models.TextField(verbose_name='\u63cf\u8ff0')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='\u521b\u5efa\u65e5\u671f')),
                ('update_date', models.DateField(auto_now=True, verbose_name='\u66f4\u65b0\u65e5\u671f')),
                ('inventory', models.IntegerField(verbose_name='\u5e93\u5b58\u91cf')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mall.Category', verbose_name='\u5546\u54c1\u7c7b\u522b')),
                ('related_products', models.ManyToManyField(to='mall.Product', verbose_name='\u76f8\u5173\u5546\u54c1')),
            ],
        ),
        migrations.CreateModel(
            name='ProductComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='\u8bc4\u4ef7\u5185\u5bb9')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('score', models.IntegerField(verbose_name='\u8bc4\u5206')),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_user', to=settings.AUTH_USER_MODEL, verbose_name='\u8d2d\u4e70\u4eba')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mall.Product', verbose_name='\u5546\u54c1\u540d')),
            ],
        ),
        migrations.CreateModel(
            name='RegisterUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_phone', models.IntegerField(verbose_name='\u624b\u673a\u53f7')),
                ('user_address', models.TextField(verbose_name='\u5730\u5740')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='register_user', to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237\u59d3\u540d')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='\u521b\u5efa\u65e5\u671f')),
                ('update_date', models.DateField(auto_now=True, verbose_name='\u66f4\u65b0\u65e5\u671f')),
                ('products', models.ManyToManyField(to='mall.Product', verbose_name='\u5546\u54c1\u540d')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_user', to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237\u540d')),
            ],
        ),
        migrations.AddField(
            model_name='orders',
            name='products',
            field=models.ManyToManyField(to='mall.Product', verbose_name='\u5546\u54c1'),
        ),
    ]
