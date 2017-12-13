# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_auto_20170717_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='gethelp',
            name='payment_made',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='gethelp',
            name='payment_received',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='providehelp',
            name='payment_made',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='providehelp',
            name='payment_received',
            field=models.BooleanField(default=False),
        ),
    ]
