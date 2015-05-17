# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=128)),
                ('desc', models.TextField()),
                ('img', models.ImageField(upload_to='image')),
            ],
        ),
        migrations.CreateModel(
            name='MySubjectRelations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('child_subject', models.CharField(max_length=128)),
                ('father_subject', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nickname', models.CharField(max_length=16)),
                ('permission', models.IntegerField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=128)),
                ('full_link', models.CharField(max_length=128)),
                ('pubDate', models.DateField()),
                ('OSTI_id', models.CharField(max_length=64)),
                ('report_num', models.CharField(max_length=64)),
                ('research_org', models.CharField(max_length=256)),
                ('sponsor_org', models.CharField(max_length=256)),
                ('resource_type', models.CharField(max_length=64)),
                ('pub_country', models.CharField(max_length=64)),
                ('record_description', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('subject_name', models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='record',
            name='record_subjects',
            field=models.ManyToManyField(to='management.Subject'),
        ),
        migrations.AddField(
            model_name='img',
            name='book',
            field=models.ForeignKey(to='management.Record'),
        ),
    ]
