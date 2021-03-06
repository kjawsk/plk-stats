# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-19 18:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0004_player_short_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action_Subtype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='action',
            name='team',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='stats.Team'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='action_type',
            name='name',
            field=models.CharField(max_length=20),
        ),
        migrations.AddField(
            model_name='action_subtype',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.Action_Type'),
        ),
        migrations.AddField(
            model_name='action',
            name='action_subtype',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='stats.Action_Subtype'),
            preserve_default=False,
        ),
    ]
