# Generated by Django 4.2 on 2024-09-23 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hernia', '0009_remove_historial_pdf_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cedula',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
