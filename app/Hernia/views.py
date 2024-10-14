import os
import subprocess
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import pytz
from .forms import ImagenForm, RegistroForm, ProfileForm, UserForm
from .models import Imagen, Profile
from app.Hernia.ia_model.predict import predict_image 
import hashlib
from django.core.files.storage import default_storage
from django.contrib.auth.views import PasswordResetCompleteView
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.paginator import Paginator
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from io import BytesIO
from .models import Historial


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    def get(self, request, *args, **kwargs):
        return redirect('login')
    

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil actualizado exitosamente')
            return redirect('profile')
        else:
            messages.error(request, 'Error al actualizar el perfil')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'editar_perfil.html', {'user_form': user_form, 'profile_form': profile_form})


def entrenar_modelo(request):
    script_path = os.path.join(settings.BASE_DIR, 'app/Hernia/ia_model/train_model.py')

    if not os.path.exists(script_path):
        return HttpResponse(f"Error: El archivo de script no se encuentra en {script_path}", status=404)

    
    result = subprocess.run(['python', script_path], capture_output=True, text=True)

    
    salida = result.stdout + "\n" + result.stderr

    return HttpResponse(f"<pre>{salida}</pre>")





@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    
    if not request.session.get('welcome_message_shown', False):
        request.session['welcome_message_shown'] = True
        show_welcome_message = True
    else:
        show_welcome_message = False

    return render(request, 'home.html', {
        'user': request.user,
        'show_welcome_message': show_welcome_message,
    })
    
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    return render(request, 'login.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)  
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)  

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'perfil.html', {'user_form': user_form, 'profile_form': profile_form})


def password_reset_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            messages.success(request, 'Se ha enviado un enlace para restablecer la contraseña a tu correo electrónico.')
            return redirect('password_reset')
        except User.DoesNotExist:
            messages.error(request, 'El correo electrónico no está registrado en nuestro sistema.')
    return render(request, 'password_reset.html')


#----------------------------


def register_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, '¡Registro exitoso! Por favor, inicia sesión.')
                return redirect('login') 
            except Exception as e:
                messages.error(request, f'Error al registrar el usuario: {e}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = RegistroForm()
    
    return render(request, 'register.html', {'form': form})





def subir_imagen(request):
    if request.method == 'POST':
        form = ImagenForm(request.POST, request.FILES)
        if form.is_valid():
            imagen_obj = form.save(commit=False)  

            
            original_name = request.FILES['imagen'].name
            hash_object = hashlib.sha256(original_name.encode())
            encrypted_name = hash_object.hexdigest() + '.' + original_name.split('.')[-1]  

            
            imagen_obj.imagen.name = encrypted_name

            imagen_obj.save()

            image_path = imagen_obj.imagen.path  

            grupo, porcentaje = predict_image(image_path)
            
            ecuador_tz = pytz.timezone('America/Guayaquil')
            fecha_imagen_local = imagen_obj.fecha.astimezone(ecuador_tz)

            context = {
                'grupo': grupo,
                'porcentaje': porcentaje,
                'imagen_url': imagen_obj.imagen.url,
                'fecha_imagen': fecha_imagen_local
            }

            historial = Historial(
                user=request.user,
                imagen=imagen_obj.imagen,
                porcentaje=porcentaje,
                grupo=grupo,
            )
            historial.save()
            
            return render(request, 'resultados.html', context)
    else:
        form = ImagenForm()

    return render(request, 'subir_imagen.html', {'form': form})



def user_profile_view(request):
    user = request.user
    profile = getattr(user, 'profile', None)

    if profile is None:
        profile = Profile.objects.create(user=user)

    return render(request, 'perfil.html', {'user': user, 'profile': profile})

