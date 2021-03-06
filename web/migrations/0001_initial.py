# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-26 06:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupName', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=200)),
                ('date', models.CharField(max_length=200)),
                ('out_name', models.CharField(max_length=200)),
                ('out', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Out',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('out_name', models.CharField(max_length=200)),
                ('out_chinese_name', models.CharField(max_length=200)),
                ('group', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IDD', models.CharField(max_length=10)),
                ('info', models.TextField()),
                ('Type', models.CharField(max_length=16)),
                ('status', models.CharField(max_length=16)),
                ('shenpi', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=50)),
                ('groupname', models.CharField(max_length=200)),
            ],
        ),
    ]
