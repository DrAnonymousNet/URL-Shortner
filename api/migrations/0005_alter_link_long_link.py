# Generated by Django 4.0.5 on 2022-07-06 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_link_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='long_link',
            field=models.URLField(max_length=255, verbose_name='Long link'),
        ),
    ]
