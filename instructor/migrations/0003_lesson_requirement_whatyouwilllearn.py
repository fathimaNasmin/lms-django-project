# Generated by Django 3.2 on 2023-09-18 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lms_main', '0049_auto_20230918_1117'),
        ('instructor', '0002_level'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
             migrations.CreateModel(
                    name='WhatYouWillLearn',
                        fields=[
                            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                            ('points', models.CharField(default='no points', max_length=500)),
                            ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms_main.course')),
                        ],
                ),
            ],
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='Requirement',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True,
                                                   primary_key=True, serialize=False, verbose_name='ID')),
                        ('requirement_points', models.CharField(
                            default='', max_length=500)),
                        ('course', models.ForeignKey(
                            on_delete=django.db.models.deletion.CASCADE, to='lms_main.course')),
                    ],
                ),
            ],
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='Lesson',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True,
                                                   primary_key=True, serialize=False, verbose_name='ID')),
                        ('name', models.CharField(max_length=200)),
                        ('course', models.ForeignKey(
                            on_delete=django.db.models.deletion.CASCADE, to='lms_main.course')),
                    ],
                ),
            ],
        ),
    ]
