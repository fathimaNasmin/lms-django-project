# Generated by Django 3.2 on 2023-08-26 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lms_main', '0024_alter_course_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitems',
            name='user_courses',
        ),
        migrations.AddField(
            model_name='orderitems',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='lms_main.course'),
        ),
    ]
