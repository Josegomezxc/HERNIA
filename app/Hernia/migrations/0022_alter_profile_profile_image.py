# Generated by Django 4.2 on 2024-10-20 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hernia', '0021_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(default='get_default_profile_image', upload_to='profile_images/'),
        ),
    ]
