# Generated by Django 4.2 on 2024-10-18 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hernia', '0012_alter_imagen_imagen_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagen',
            name='imagen',
            field=models.ImageField(upload_to='imagenes/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(default='images/usuario-logo2.png', upload_to='profile_images/'),
        ),
    ]
