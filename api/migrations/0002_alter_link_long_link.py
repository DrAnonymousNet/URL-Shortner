# Generated by Django 4.0.5 on 2022-06-29 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='long_link',
            field=models.URLField(verbose_name='Long link'),
        ),
    ]
