# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-19 07:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mips', '0019_auto_20180319_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='regnum',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
