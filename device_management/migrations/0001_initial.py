# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-05 07:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='device_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_user', models.IntegerField()),
                ('brands', models.CharField(max_length=128)),
                ('MODEL', models.CharField(max_length=128)),
                ('serial_numbers', models.CharField(max_length=128)),
                ('count', models.IntegerField()),
                ('attri', models.CharField(max_length=128)),
                ('info', models.TextField()),
                ('usage', models.CharField(max_length=256)),
            ],
        ),
    ]
