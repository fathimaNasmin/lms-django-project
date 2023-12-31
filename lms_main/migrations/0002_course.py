# Generated by Django 3.2 on 2023-08-14 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_rename_about_instructor_about_me'),
        ('lms_main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('featured_image', models.ImageField(null=True, upload_to='course/featured_images/')),
                ('featured_video', models.CharField(max_length=500)),
                ('price', models.IntegerField(default=0, null=True)),
                ('discount', models.IntegerField(null=True)),
                ('slug', models.SlugField(blank=True, default='', max_length=400, null=True)),
                ('status', models.CharField(choices=[('PUBLISH', 'PUBLISH'), ('DRAFT', 'DRAFT')], max_length=100, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.instructor')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms_main.category')),
            ],
        ),
    ]
