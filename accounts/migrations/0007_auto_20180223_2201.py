# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20180223_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='email_validation_expire',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 28, 22, 1, 54, 607000)),
        ),
        migrations.AlterField(
            model_name='workindustry',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 23, 21, 1, 54, 597000, tzinfo=utc)),
        ),
    ]
