# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-10 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0013_auto_20170510_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='type',
            field=models.IntegerField(default=1),
        ),
    ]