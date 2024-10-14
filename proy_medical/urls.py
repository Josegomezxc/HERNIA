# urls.py

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.Hernia import views
from django.contrib.auth import views as auth_views

from app.Hernia.forms import CustomPasswordResetForm

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'), 
    path('subir/', views.subir_imagen, name='subir_imagen'),
    
    path('perfil/', views.profile_view, name='profile'),
    path('entrenar_modelo/', views.entrenar_modelo, name='entrenar_modelo'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),

    
    # URLs para el restablecimiento de contraseñas
    path('password_reset/', auth_views.PasswordResetView.as_view(
        form_class=CustomPasswordResetForm,  # Usar el formulario personalizado
        template_name='password_reset.html',
        subject_template_name='password_reset_subject.txt',  # Plantilla del asunto
        email_template_name='password_reset_email.html'  # Plantilla del correo
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
