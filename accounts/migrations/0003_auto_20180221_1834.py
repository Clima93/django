# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180221_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='email_validation_expire',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 26, 18, 34, 5, 679000)),
        ),
        migrations.AlterField(
            model_name='workindustry',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 21, 17, 34, 5, 670000, tzinfo=utc)),
        ),
    ]
