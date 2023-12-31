# Generated by Django 3.2 on 2023-09-15 04:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lms_main', '0042_auto_20230912_0940'),
        ('user', '0011_alter_enrolledcourses_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayingVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pause_time', models.FloatField(blank=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms_main.course')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms_main.lesson')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.student')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms_main.video')),
            ],
        ),
    ]
