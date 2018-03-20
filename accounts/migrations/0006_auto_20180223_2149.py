# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20180223_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='email_validation_expire',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 28, 21, 49, 32, 698000)),
        ),
        migrations.AlterField(
            model_name='workindustry',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 23, 20, 49, 32, 689000, tzinfo=utc)),
        ),
    ]
