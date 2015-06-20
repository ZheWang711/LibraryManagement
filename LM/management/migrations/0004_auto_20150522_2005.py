# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_mynews'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='author',
            field=models.CharField(max_length=128, default='unknown'),
        ),
        migrations.AlterField(
            model_name='mynews',
            name='link',
            field=models.CharField(max_length=128, default='NULL'),
        ),
    ]
