# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-08 07:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faults_record', '0006_auto_20161008_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fault_info',
            name='create_time',
            field=models.DateField(),
        ),
    ]
