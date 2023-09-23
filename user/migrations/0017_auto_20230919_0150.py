# Generated by Django 3.2 on 2023-09-19 01:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0005_auto_20230919_0150'),
        ('user', '0016_auto_20230918_1359'),
    ]

    operations = [
        # migrations.AlterField(
        #     model_name='playingvideo',
        #     name='course',
        #     field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.course'),
        # ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='playingvideo',
                    name='course',
                    field=models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to='instructor.course'),
                ),
            ],
        ),
        # migrations.AlterField(
        #     model_name='playingvideo',
        #     name='lesson',
        #     field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.lesson'),
        # ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='playingvideo',
                    name='lesson',
                    field=models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to='instructor.lesson'),
                ),
            ],
        ),
        # migrations.AlterField(
        #     model_name='playingvideo',
        #     name='video',
        #     field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.video'),
        # ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='playingvideo',
                    name='video',
                    field=models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to='instructor.video'),
                ),
            ],
        ),
    ]