# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-08 12:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pywims_exos', '0006_auto_20170608_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exo',
            name='layout',
            field=models.CharField(choices=[('STD', 'Standard'), ('GGB', 'Geogebra')], default='STD', max_length=3),
        ),
    ]