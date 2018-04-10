# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-10 15:39
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
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=5000)),
                ('praise', models.IntegerField(default=0)),
                ('coll', models.IntegerField(default=0)),
                ('zf_num', models.IntegerField(default=0)),
                ('pl_num', models.IntegerField(default=0)),
                ('add_time', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'forum_article',
                'verbose_name': '\u6587\u7ae0\u4e3b\u8868',
            },
        ),
        migrations.CreateModel(
            name='ArticleTalk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000)),
                ('uid', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=0)),
                ('l_id', models.IntegerField(default=0)),
                ('praise', models.IntegerField(default=0)),
                ('add_time', models.IntegerField(default=0)),
                ('aid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Article')),
            ],
            options={
                'db_table': 'forum_article_talk',
                'verbose_name': '\u8bc4\u8bba\u8868',
            },
        ),
        migrations.CreateModel(
            name='LiuYan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('add_time', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'forum_ly',
                'verbose_name': '\u7559\u8a00\u8868',
            },
        ),
        migrations.CreateModel(
            name='Praise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(default=0)),
                ('uid', models.IntegerField(default=0)),
                ('artcile', models.IntegerField(default=0)),
                ('num', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'forum_article_praise',
                'verbose_name': '\u70b9\u8d5e\u8868',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20)),
                ('addtime', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'forum_tags',
                'verbose_name': '\u5206\u7c7b\u8868',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Tags'),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]