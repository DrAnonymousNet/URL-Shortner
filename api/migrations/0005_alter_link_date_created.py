# Generated by Django 4.0.5 on 2022-07-26 14:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_link_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='date_created',
            field=models.DateField(default=django.utils.timezone.localtime),
        ),
    ]
