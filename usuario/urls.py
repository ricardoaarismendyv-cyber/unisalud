from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_unisalud, name='inicio_unisalud'),
    path('login-us', views.loginus, name='login-us'),
    path('inicio-us', views.iniciousuario, name='inicio-usuario'),
    path('historia-clinica', views.hcusuario, name='hcusuario'),
    path('ordenes-medicas', views.omusuario, name='omusuario'),
    path('ordenes-medicamentos', views.omeusuario, name='omeusuario'),
    path('turnos', views.turnosusuario, name='turnos-usuario'),
    path('preguntas-frecuentes', views.preguntasfrecuentes, name='preguntas-frecuentes'),
    path('uso-del-sistema', views.usosistema, name='usosistema'),
    path('buzon-sugerencias', views.buzonsugerencias, name='buzonsugerencias'),
    path('registrarse', views.registro, name='registrarse'),
    path('contactanos', views.contactanos, name='contactanos')
]

