# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-27 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0015_auto_20170924_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='vat',
            field=models.DecimalField(decimal_places=0, default=0, help_text='If you are VAT registered set this to 15 else leave at 0', max_digits=2, verbose_name='VAT %'),
        ),
    ]
