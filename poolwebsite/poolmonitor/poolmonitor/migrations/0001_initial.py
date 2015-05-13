# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('reading_type', models.CharField(choices=[('temp', 'Temperature'), ('pH', 'Acidity')], max_length=4, verbose_name='Reading Type')),
                ('reading', models.IntegerField(default=15, verbose_name='Reading Value')),
                ('reading_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Reading Date')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('description_text', models.CharField(max_length=255, verbose_name='Sensor Description')),
                ('file_system_location', models.CharField(primary_key=True, verbose_name='File System location of Sensor in /sys/bus/w1/devices/', default='28-nnnnn', max_length=50, help_text="To determine your device run 'ls /sys/bus/w1/devices and look for items with 28- in their name'", serialize=False)),
                ('pooling_interval', models.IntegerField(default=15, verbose_name='Frequency to check temperature in minutes')),
                ('location_image', models.ImageField(blank=True, verbose_name='Optional image of location', upload_to='')),
            ],
        ),
        migrations.AddField(
            model_name='reading',
            name='sensor',
            field=models.ForeignKey(to='poolmonitor.Sensor'),
        ),
    ]
