# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-08 03:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('choose_electricity', '0002_priceplan_other_cost_eqn'),
    ]

    operations = [
        migrations.AddField(
            model_name='priceplan',
            name='tlf',
            field=models.DecimalField(decimal_places=0, default=1, max_digits=1, verbose_name='TLF'),
            preserve_default=False,
        ),
    ]
