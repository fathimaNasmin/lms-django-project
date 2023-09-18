# Generated by Django 3.2 on 2023-09-18 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0002_level'),
        ('lms_main', '0048_auto_20230918_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.level'),
        ),
        # migrations.DeleteModel(
        #     name='Level',
        # ),
        
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name='Level',
                ),
            ],
                    database_operations=[
             migrations.AlterModelTable(
                 name='Level',
                                    table='instructor_level',
                ),
            ],
        )
    ]
