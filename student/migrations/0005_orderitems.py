# Generated by Django 3.2 on 2023-09-18 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lms_main', '0047_delete_orderitems'),
        ('user', '0014_delete_enrolledcourses'),
        ('student', '0004_order'),
    ]

    operations = [
        # migrations.CreateModel(
        #     name='OrderItems',
        #     fields=[
        #         ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('item_price', models.IntegerField(default=0, null=True)),
        #         ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms_main.course')),
        #         ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.order')),
        #         ('student', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='user.student')),
        #     ],
        #     options={
        #         'unique_together': {('course', 'order', 'student')},
        #     },
        # ),
        
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='OrderItems',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('item_price', models.IntegerField(default=0, null=True)),
                        ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms_main.course')),
                        ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.order')),
                        ('student', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='user.student')),
                    ],
                    options={
                        'unique_together': {('course', 'order', 'student')},
                    },
                ),
            ]
        )
    ]
