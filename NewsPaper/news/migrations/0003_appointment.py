# Generated by Django 4.1.3 on 2023-12-20 12:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_post_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime(2023, 12, 20, 15, 33, 59, 775031))),
                ('client_name', models.CharField(max_length=200)),
                ('message', models.TextField()),
            ],
        ),
    ]
