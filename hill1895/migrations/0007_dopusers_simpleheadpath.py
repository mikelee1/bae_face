# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2018-03-12 09:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hill1895', '0006_dopusers_inuse'),
    ]

    operations = [
        migrations.AddField(
            model_name='dopusers',
            name='simpleheadpath',
            field=models.CharField(default=b'null', max_length=250),
        ),
    ]