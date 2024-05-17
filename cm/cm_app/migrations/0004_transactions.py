# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2022-09-20 11:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cm_app', '0003_files'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('t_id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('sender_name', models.CharField(max_length=255)),
                ('sender_address', models.CharField(max_length=255)),
                ('receiver_name', models.CharField(max_length=255)),
                ('receiver_address', models.CharField(max_length=255)),
                ('transaction_hash', models.CharField(max_length=255)),
            ],
        ),
    ]