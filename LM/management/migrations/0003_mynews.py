# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_auto_20150516_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyNews',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('content', models.CharField(max_length=2048)),
                ('link', models.CharField(max_length=128)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='data published')),
            ],
        ),
    ]
