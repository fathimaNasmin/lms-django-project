# Generated by Django 3.2 on 2023-08-27 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_enrolledcourses_unique_together'),
        ('lms_main', '0033_order_pdf_receipt'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitems',
            name='student',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='user.student'),
        ),
        migrations.AlterUniqueTogether(
            name='orderitems',
            unique_together={('course', 'order', 'student')},
        ),
    ]
