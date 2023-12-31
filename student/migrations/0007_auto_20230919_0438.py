# Generated by Django 3.2 on 2023-09-19 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0007_auto_20230919_0438'),
        ('user', '0018_delete_playingvideo'),
        ('student', '0006_auto_20230918_1359'),
    ]

    operations = [
        # migrations.AlterField(
        #     model_name='cart',
        #     name='course',
        #     field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.course'),
        # ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='cart',
                    name='course',
                    field=models.ForeignKey(
                         on_delete=django.db.models.deletion.PROTECT, to='instructor.course'),
                ),
            ],
        ),
        # migrations.AlterField(
        #     model_name='enrolledcourses',
        #     name='course',
        #     field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.course'),
        # ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='enrolledcourses',
                    name='course',
                    field=models.ForeignKey(
                         on_delete=django.db.models.deletion.PROTECT, to='instructor.course'),
                ),
            ],
        ),
        # migrations.AlterField(
        #     model_name='orderitems',
        #     name='course',
        #     field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.course'),
        # ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='orderitems',
                    name='course',
                    field=models.ForeignKey(
                         on_delete=django.db.models.deletion.PROTECT, to='instructor.course'),
                ),
            ],
        ),
        # migrations.AlterField(
        #     model_name='saveforlater',
        #     name='course',
        #     field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.course'),
        # ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='saveforlater',
                    name='course',
                    field=models.ForeignKey(
                         on_delete=django.db.models.deletion.PROTECT, to='instructor.course'),
                ),
            ],
        ),
        # migrations.CreateModel(
        #     name='PlayingVideo',
        #     fields=[
        #         ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('pause_time', models.FloatField(blank=True, null=True)),
        #         ('updated_time', models.DateTimeField(auto_now_add=True)),
        #         ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.course')),
        #         ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.lesson')),
        #         ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.student')),
        #         ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.video')),
        #     ],
        # ),
        
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='PlayingVideo',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('pause_time', models.FloatField(blank=True, null=True)),
                        ('updated_time', models.DateTimeField(auto_now_add=True)),
                        ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.course')),
                        ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.lesson')),
                        ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.student')),
                        ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.video')),
                    ],
                    ),
                ],
                        # Table already exists. See catalog/migrations/0003_delete_product.py
             database_operations=[],
        ),
    ]
