# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-19 19:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0005_auto_20171119_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='action_subtype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stats.Action_Subtype'),
        ),
    ]
