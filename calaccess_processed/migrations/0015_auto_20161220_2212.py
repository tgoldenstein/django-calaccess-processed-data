# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-20 22:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calaccess_processed', '0014_auto_20161216_0534'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='election',
            name='year',
        ),
        migrations.AlterField(
            model_name='election',
            name='election_date',
            field=models.DateField(help_text='Date of the election', verbose_name='election date'),
        ),
    ]