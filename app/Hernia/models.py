from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Imagen(models.Model):
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagenes/')
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', default='/app/Hernia/static/images/usuario-logo2.png')
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    cedula = models.CharField(max_length=20, blank=True, null=True, unique=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Historial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_imagen = models.DateTimeField(auto_now_add=True)  # Puedes usar auto_now_add si quieres que se añada automáticamente cuando se guarda
    imagen = models.ImageField(upload_to='historial_imagenes/', blank=True, null=True)
    porcentaje = models.FloatField()
    grupo = models.CharField(max_length=255)
    fecha_imagen = models.DateTimeField(auto_now_add=True)  # Para registrar la fecha en la que se guardó el historial

    def __str__(self):
        return f'{self.user.username} - {self.fecha_imagen}'



