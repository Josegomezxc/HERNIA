# Generated by Django 4.2 on 2024-09-23 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hernia', '0010_profile_cedula_alter_profile_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
