# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-30 11:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0004_circuit_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='circuit',
            name='no',
            field=models.PositiveIntegerField(),
        ),
    ]