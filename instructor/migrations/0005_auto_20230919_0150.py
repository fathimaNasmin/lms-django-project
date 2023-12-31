# Generated by Django 3.2 on 2023-09-19 01:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0004_auto_20230918_1359'),
    ]

    operations = [
        # migrations.AlterField(
        #     model_name='lesson',
        #     name='course',
        #     field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.course'),
        # ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='lesson',
                    name='course',
                    field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='instructor.course'),
                ),
            ],
        ),
        
        # migrations.AlterField(
        #     model_name='requirement',
        #     name='course',
        #     field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.course'),
        # ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='requirement',
                    name='course',
                    field=models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to='instructor.course'),
                ),
            ],
        ),
        # migrations.AlterField(
        #     model_name='whatyouwilllearn',
        #     name='course',
        #     field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.course'),
        # ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='whatyouwilllearn',
                    name='course',
                    field=models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to='instructor.course'),
                ),
            ],
        ),
        # migrations.CreateModel(
        #     name='Video',
        #     fields=[
        #         ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('title', models.CharField(max_length=100)),
        #         ('video_file', models.FileField(blank=True, null=True, upload_to='videos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])),
        #         ('time_duration', models.FloatField(blank=True, null=True)),
        #         ('upload_date', models.DateTimeField(auto_now_add=True)),
        #         ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.course')),
        #         ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.lesson')),
        #     ],
        # ),
        
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='Video',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('title', models.CharField(max_length=100)),
                        ('video_file', models.FileField(blank=True, null=True, upload_to='videos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])),
                        ('time_duration', models.FloatField(blank=True, null=True)),
                        ('upload_date', models.DateTimeField(auto_now_add=True)),
                        ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.course')),
                        ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.lesson')),
                    ],
                ),
            ],
        ),
    ]
