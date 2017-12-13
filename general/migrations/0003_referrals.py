# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0002_useraccount_referral'),
    ]

    operations = [
        migrations.CreateModel(
            name='Referrals',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=50, null=True, blank=True)),
                ('user', models.ForeignKey(blank=True, to='general.UserAccount', null=True)),
            ],
        ),
    ]
