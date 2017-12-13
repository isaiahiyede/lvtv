# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0003_referrals'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='referrals',
            options={'ordering': ['-created_on'], 'verbose_name_plural': 'Referrals'},
        ),
        migrations.AddField(
            model_name='referrals',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 29, 10, 20, 46, 786547, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
