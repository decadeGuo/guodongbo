# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-06 14:55
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
            name='LeaveDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(default=1, verbose_name='\u65b9\u5f0f')),
                ('resign', models.CharField(default='', max_length=200, verbose_name='\u539f\u56e0')),
                ('days', models.FloatField(default=1, verbose_name='\u5929\u6570')),
                ('sp_id', models.IntegerField(default=0, verbose_name='\u5ba1\u6279\u4eba')),
                ('begain_time', models.IntegerField(default=0, verbose_name='\u5f00\u59cb\u65f6\u95f4')),
                ('end_time', models.IntegerField(default=0, verbose_name='\u7ed3\u675f\u65f6\u95f4')),
                ('status', models.IntegerField(default=0, verbose_name='\u5ba1\u6279\u7ed3\u679c')),
                ('remark', models.CharField(default='', max_length=200, verbose_name='\u62d2\u63a5\u539f\u56e0')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'leave_detail',
                'verbose_name': '\u8bf7\u5047\u8be6\u60c5\u8868',
            },
        ),
    ]