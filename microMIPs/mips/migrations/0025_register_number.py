# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-19 07:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mips', '0024_remove_register_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='number',
            field=models.PositiveIntegerField(default=0),
        ),
    ]