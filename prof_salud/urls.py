from django.urls import path, include
from usuario import views as usuario_views
from administrativo import views as admin_views
from . import views


urlpatterns = [ 
    path('inicio_prof_salud/', views.inicio_prof_salud, name='inicio_prof_salud'),
    path('paciente/logout_prof_salud/historia_clinica/', views.hc_prof_salud, name='hc_prof_salud'),
    path('historia_clinica/', views.hc_prof_salud, name='hc_prof_salud'),
    path('ordenes_medicas/', views.om_prof_salud, name='om_prof_salud'),
    path('ordenes_medicamentos/', views.omed_prof_salud, name='omed_prof_salud'),
    path('turnos/', views.consultas_prof_salud, name='consultas_prof_salud'),
    path('preguntas-frecuentes', views.preguntasfrecuentes_prof_salud, name='preguntas-frecuentes_prof_salud'),
    path('uso-del-sistema', views.usosistema_prof_salud, name='usosistema_prof_salud'),
    path('buzon-sugerencias', views.buzonsugerencias_prof_salud, name='buzonsugerencias_prof_salud'),
    path('registrarse/', views.registro_prof_salud, name='registro_prof_salud'),
    path('contactanos', views.contactanos_prof_salud, name='contactanos_prof_salud')
]
