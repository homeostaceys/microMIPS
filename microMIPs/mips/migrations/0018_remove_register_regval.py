# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-19 07:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mips', '0017_auto_20180319_1518'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register',
            name='regval',
        ),
    ]