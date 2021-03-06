# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-18 17:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20171117_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='department',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='assignment_department', to='core.Department'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='assignment_session', to='core.Session', unique=True),
        ),
    ]
