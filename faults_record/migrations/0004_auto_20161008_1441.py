# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-08 06:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faults_record', '0003_auto_20161008_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fault_info',
            name='create_time',
            field=models.DateField(default=datetime.date(2016, 10, 8)),
        ),
    ]
