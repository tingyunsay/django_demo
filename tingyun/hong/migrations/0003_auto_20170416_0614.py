# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-16 06:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hong', '0002_auto_20170416_0552'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hong',
            old_name='cmpany',
            new_name='company',
        ),
    ]
