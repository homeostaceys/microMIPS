# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-28 07:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mips', '0031_auto_20180325_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piplnsrcdest',
            name='label',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]