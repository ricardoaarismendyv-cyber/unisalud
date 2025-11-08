from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.login_admin, name='login_admin'),
    path('inicio_admin/', views.inicio_admin, name='inicio_admin'),
    path('historia_clinica/', views.hc_admin, name='hc_admin'),
    path('ordenes_medicas/', views.om_admin, name='om_admin'),
    path('ordenes_medicamentos/', views.omed_admin, name='omed_admin'),
    path('turnos/', views.turnos_admin, name='turnos_admin'),
    path('preguntas-frecuentes/', views.preguntasfrecuentes_admin, name='preguntas-frecuentes_admin'),
    path('uso-del-sistema', views.usosistema_admin, name='usosistema_admin'),
    path('buzon-sugerencias', views.buzonsugerencias_admin, name='buzonsugerencias_admin'),
    path('registrarse/', views.registro_admin, name='registro_admin'),
    path('contactanos', views.contactanos_admin, name='contactanos_admin'),
    path('gestion/', views.gestion_admin, name='gestion_admin'),
]
