# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-19 11:04
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
            name='Car_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, verbose_name='\u8f66\u8f86\u540d\u5b57')),
                ('card', models.CharField(default='', max_length=20, verbose_name='\u8f66\u724c\u53f7')),
                ('status', models.IntegerField(default=1, verbose_name='\u72b6\u6001')),
                ('add_time', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'car_info',
                'verbose_name': '\u8f66\u8f86\u8868',
            },
        ),
        migrations.CreateModel(
            name='UserCarDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resign', models.CharField(max_length=2000, verbose_name='\u539f\u56e0')),
                ('peo_num', models.IntegerField(default=0, verbose_name='\u4eba\u6570')),
                ('toplace', models.CharField(max_length=200, verbose_name='\u5230\u8fbe\u5730\u70b9')),
                ('people_ids', models.CharField(default='', max_length=1000, verbose_name='\u4e58\u8f66\u4eba')),
                ('status', models.CharField(default='', max_length=5000, verbose_name='\u7533\u8bf7\u72b6\u6001')),
                ('begain_time', models.IntegerField(default=0)),
                ('end_time', models.IntegerField(default=0)),
                ('add_time', models.IntegerField(default=0)),
                ('update_time', models.IntegerField(default=0)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='use_car.Car_info')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_car_detail',
                'verbose_name': '\u7528\u8f66\u8868',
            },
        ),
    ]
