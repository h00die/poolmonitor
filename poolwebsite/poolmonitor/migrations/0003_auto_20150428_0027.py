# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poolmonitor', '0002_auto_20150427_0100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reading',
            name='reading_type',
        ),
        migrations.AddField(
            model_name='sensor',
            name='reading_type',
            field=models.CharField(default='temp', verbose_name='Reading Type', max_length=4, choices=[('temp', 'Temperature'), ('pH', 'Acidity')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reading',
            name='reading',
            field=models.IntegerField(verbose_name='Reading Value'),
        ),
    ]
