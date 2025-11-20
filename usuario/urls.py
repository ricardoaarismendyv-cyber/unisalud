from django.urls import path
from . import views


urlpatterns = [
    # Las URLs de login y logout son manejadas por la app 'login'
    path('', views.inicio_usuario, name='inicio-usuario'),
    path('historia-clinica', views.hcusuario, name='hcusuario'),
    path('ordenes-medicas', views.omusuario, name='omusuario'),
    path('ordenes-medicamentos', views.omeusuario, name='omeusuario'),
    path('turnos', views.turnosusuario, name='turnos-usuario'),
    path('preguntas-frecuentes', views.preguntasfrecuentes, name='preguntas-frecuentes'),
    path('uso-del-sistema', views.usosistema, name='usosistema'),
    path('buzon-sugerencias', views.buzonsugerencias, name='buzonsugerencias'),
    path('registrarse', views.registro, name='registrarse'),
    path('contactanos', views.contactanos, name='contactanos'),
]
