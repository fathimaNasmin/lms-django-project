# Generated by Django 3.2 on 2023-08-20 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms_main', '0016_auto_20230820_0147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='time_duration',
            field=models.FloatField(blank=True, null=True),
        ),
    ]