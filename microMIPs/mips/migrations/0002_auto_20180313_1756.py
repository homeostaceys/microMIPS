# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-13 09:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mips', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opcodetable',
            name='rd',
        ),
        migrations.RemoveField(
            model_name='opcodetable',
            name='rs',
        ),
        migrations.RemoveField(
            model_name='opcodetable',
            name='rt',
        ),
        migrations.RemoveField(
            model_name='opcodetable',
            name='variable',
        ),
    ]