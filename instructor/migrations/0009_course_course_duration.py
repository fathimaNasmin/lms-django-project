# Generated by Django 3.2 on 2023-09-24 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0008_auto_20230922_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_duration',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]