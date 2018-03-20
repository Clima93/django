# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20180221_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='email_validation_expire',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 28, 21, 10, 45, 441000)),
        ),
        migrations.AlterField(
            model_name='workindustry',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 23, 20, 10, 45, 432000, tzinfo=utc)),
        ),
    ]
