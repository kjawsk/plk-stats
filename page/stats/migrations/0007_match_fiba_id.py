# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-20 18:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0006_auto_20171119_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='fiba_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
