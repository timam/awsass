# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-18 19:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20171118_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
