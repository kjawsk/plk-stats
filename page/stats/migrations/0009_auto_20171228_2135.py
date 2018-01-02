# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-28 21:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0008_remove_action_subtype_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Period_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=8)),
            ],
        ),
        migrations.AddField(
            model_name='action',
            name='period',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='action',
            name='success',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='action',
            name='period_type',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='stats.Period_Type'),
            preserve_default=False,
        ),
    ]