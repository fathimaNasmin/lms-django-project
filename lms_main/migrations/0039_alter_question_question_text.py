# Generated by Django 3.2 on 2023-09-04 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms_main', '0038_question_quizoption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(max_length=300),
        ),
    ]
