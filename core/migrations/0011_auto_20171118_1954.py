# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-18 19:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20171118_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='name',
            field=models.TextField(max_length=256),
        ),
    ]
