# Generated by Django 4.0.5 on 2022-07-22 19:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='long_link',
            field=models.TextField(max_length=1000, validators=[django.core.validators.URLValidator], verbose_name='Long link'),
        ),
    ]