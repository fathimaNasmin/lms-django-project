# Generated by Django 3.2 on 2023-08-27 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms_main', '0032_alter_order_order_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='pdf_receipt',
            field=models.FileField(blank=True, null=True, upload_to='receipts/'),
        ),
    ]
