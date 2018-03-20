# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('description', models.TextField(null=True)),
                ('image', models.ImageField(max_length=500, null=True, upload_to='uploads')),
                ('sub_title', models.CharField(max_length=500, blank=True)),
                ('html', ckeditor_uploader.fields.RichTextUploadingField()),
                ('author', models.CharField(max_length=100, null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('on_homepage', models.BooleanField(default=False)),
                ('popular', models.BooleanField(default=False)),
                ('top_article', models.BooleanField(default=False)),
                ('slug', models.SlugField(unique=True, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('parent', models.CharField(max_length=100, null=True, blank=True)),
                ('active', models.BooleanField(default=False)),
                ('country', models.BooleanField(default=False)),
                ('country_name', models.CharField(max_length=100, null=True, blank=True)),
                ('country_code', models.CharField(max_length=10, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewsLetterEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(unique=True, max_length=100)),
                ('active', models.BooleanField(default=True)),
                ('registered', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('author', models.CharField(max_length=500, blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceAlert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(unique=True, max_length=100)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
