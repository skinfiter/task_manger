# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-26 08:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_task_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='IDD',
            field=models.CharField(max_length=32),
        ),
    ]
