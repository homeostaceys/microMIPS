# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-19 07:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mips', '0018_remove_register_regval'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register',
            name='regnum',
        ),
        migrations.AddField(
            model_name='register',
            name='regval',
            field=models.CharField(default='0000000000000000', max_length=16),
        ),
    ]
