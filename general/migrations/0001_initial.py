# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password2', models.CharField(max_length=50, null=True, blank=True)),
                ('phone_number', models.CharField(max_length=15, null=True, blank=True)),
                ('title', models.CharField(max_length=50, null=True, blank=True)),
                ('address1', models.CharField(max_length=250, null=True, blank=True)),
                ('address2', models.CharField(max_length=250, null=True, blank=True)),
                ('city', models.CharField(max_length=250, null=True, blank=True)),
                ('state', models.CharField(max_length=250, null=True, blank=True)),
                ('country', models.CharField(max_length=250, null=True, blank=True)),
                ('created_on', models.DateTimeField(null=True, blank=True)),
                ('edited_on', models.DateTimeField(null=True, blank=True)),
                ('deleted_on', models.DateTimeField(null=True, blank=True)),
                ('updated_on', models.DateTimeField(null=True, blank=True)),
                ('completed', models.BooleanField(default=False)),
                ('profile_up_to_date', models.BooleanField(default=False)),
                ('bank_acc_number', models.CharField(max_length=150, null=True, blank=True)),
                ('bank_name', models.CharField(max_length=150, null=True, blank=True)),
                ('block', models.BooleanField(default=False)),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
