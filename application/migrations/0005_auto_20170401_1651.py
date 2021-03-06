# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 11:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_remove_album_publish_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='cover_url',
            new_name='cover_image',
        ),
        migrations.RemoveField(
            model_name='album',
            name='feature',
        ),
        migrations.AddField(
            model_name='album',
            name='m_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='album',
            name='release_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
