# Generated by Django 3.2 on 2023-08-18 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms_main', '0006_alter_course_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=300, null=True),
        ),
    ]