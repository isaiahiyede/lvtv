# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gethelp',
            name='help_provided',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='providehelp',
            name='help_provided',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='gethelp',
            name='package',
            field=models.CharField(blank=True, max_length=250, null=True, choices=[(b'', b'S\xc3\xa9lectionnez le paquet'), (b'50000', b'50000'), (b'100000', b'100000'), (b'200000', b'200000'), (b'500000', b'500000'), (b'1000000', b'1000000')]),
        ),
        migrations.AlterField(
            model_name='providehelp',
            name='package',
            field=models.CharField(blank=True, max_length=250, null=True, choices=[(b'', b'S\xc3\xa9lectionnez le paquet'), (b'50000', b'50000'), (b'100000', b'100000'), (b'200000', b'200000'), (b'500000', b'500000'), (b'1000000', b'1000000')]),
        ),
    ]
