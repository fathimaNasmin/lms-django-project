# Generated by Django 3.2 on 2023-08-19 00:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lms_main', '0013_alter_requirement_requirement_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='WhatYouWillLearn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.CharField(default='no points', max_length=500)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms_main.course')),
            ],
        ),
    ]
