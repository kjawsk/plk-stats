# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-21 18:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0019_auto_20180121_1759'),
    ]

    operations = [
        migrations.RenameField(
            model_name='set',
            old_name='teamplayers_set',
            new_name='teamplayers',
        ),
    ]
