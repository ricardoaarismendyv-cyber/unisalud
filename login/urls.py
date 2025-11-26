from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # Importa las vistas de autenticación de Django

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # URLs para el restablecimiento de contraseña
    # Vista para solicitar el correo de restablecimiento
    path('password_reset/', 
        auth_views.PasswordResetView.as_view(template_name='paginas/restablecimiento_contrasena.html'), 
        name='password_reset'),
    # Vista de confirmación de que el correo fue enviado
    path('password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='paginas/restablecimiento_done.html'), 
        name='password_reset_done'),

    # Vista del enlace que llega en el correo, para cambiar la contraseña
    #reset: ayuda a identificar que esta dirección es para confirmar un restablecimiento de contraseña.
    #<uidb64>: 
    # uid:  Es el número de ID único que tiene el usuario en tu base de datos.
    # b64: Significa "Base64". El ID del usuario se codifica en formato Base64. Esto no es por seguridad, sino para asegurar que el ID se pueda transmitir de forma segura en una URL sin caracteres extraños.
    #<token>: es un token único generado para la solicitud de restablecimiento de contraseña. Este token asegura que la solicitud es válida y no ha sido manipulada.
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='paginas/restablecimiento_confirm.html'), 
        name='password_reset_confirm'),

    # Vista de confirmación de que la contraseña se cambió con éxito
    path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='paginas/restablecimiento_complete.html'), 
        name='password_reset_complete'),
]
