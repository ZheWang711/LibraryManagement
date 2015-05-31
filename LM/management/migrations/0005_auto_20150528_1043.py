# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_auto_20150522_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='OSTI_id',
            field=models.CharField(default='unknown', max_length=64),
        ),
        migrations.AlterField(
            model_name='record',
            name='full_link',
            field=models.CharField(default='unknown', max_length=128),
        ),
        migrations.AlterField(
            model_name='record',
            name='pub_country',
            field=models.CharField(default='unknown', max_length=64),
        ),
        migrations.AlterField(
            model_name='record',
            name='record_description',
            field=models.CharField(default='unknown', max_length=1024),
        ),
        migrations.AlterField(
            model_name='record',
            name='report_num',
            field=models.CharField(default='unknown', max_length=64),
        ),
        migrations.AlterField(
            model_name='record',
            name='research_org',
            field=models.CharField(default='unknown', max_length=256),
        ),
        migrations.AlterField(
            model_name='record',
            name='resource_type',
            field=models.CharField(default='unknown', max_length=64),
        ),
        migrations.AlterField(
            model_name='record',
            name='sponsor_org',
            field=models.CharField(default='unknown', max_length=256),
        ),
    ]
