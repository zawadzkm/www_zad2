# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-30 11:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0003_auto_20170328_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='circuit',
            name='no',
            field=models.PositiveIntegerField(default=0, unique=True),
            preserve_default=False,
        ),
    ]
