# Generated by Django 4.0.5 on 2022-07-05 11:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_refer_analytic_referer_link_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='date_created',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]