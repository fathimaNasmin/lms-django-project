# Generated by Django 3.2 on 2023-08-14 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_instructor_about'),
    ]

    operations = [
        migrations.RenameField(
            model_name='instructor',
            old_name='about',
            new_name='about_me',
        ),
    ]
