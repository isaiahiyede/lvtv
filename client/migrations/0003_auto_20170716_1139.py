# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_auto_20170707_0939'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gethelp',
            options={'verbose_name_plural': 'Get Help'},
        ),
        migrations.AlterModelOptions(
            name='providehelp',
            options={'verbose_name_plural': 'Provide Help'},
        ),
    ]
