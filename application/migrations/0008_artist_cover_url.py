# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 12:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_remove_artist_cover_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='cover_url',
            field=models.TextField(default=None),
        ),
    ]
