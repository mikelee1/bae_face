# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2018-03-07 05:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hill1895', '0003_dopusers_userextension'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dopusers',
            name='headpath',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='dopusers',
            name='nichname',
            field=models.CharField(max_length=50),
        ),
    ]