# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20180223_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='email_validation_expire',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 28, 21, 46, 44, 886000)),
        ),
        migrations.AlterField(
            model_name='workindustry',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 23, 20, 46, 44, 876000, tzinfo=utc)),
        ),
    ]
