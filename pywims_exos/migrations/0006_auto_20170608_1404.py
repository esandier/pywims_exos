# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-08 12:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pywims_exos', '0005_auto_20170606_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exo',
            name='layout',
            field=models.FilePathField(default='C:\\Etienne\\Python\\djangogirls\\pywims_exos/templates/pywims_exos/layouts/layout_standard.html', path='C:\\Etienne\\Python\\djangogirls\\pywims_exos/templates/pywims_exos/layouts'),
        ),
    ]