# Generated by Django 3.2 on 2023-09-04 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lms_main', '0037_remove_video_serial_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField(max_length=300)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms_main.course')),
            ],
        ),
        migrations.CreateModel(
            name='QuizOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.TextField(max_length=200)),
                ('is_answer', models.BooleanField(default=False)),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms_main.question')),
            ],
        ),
    ]
