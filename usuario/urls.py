from django.urls import path
from . import views


urlpatterns = [
    # Inicio y navegación principal
    path('', views.inicio_usuario, name='inicio-usuario'),
    
    # Historia clínica
    path('historia-clinica/', views.hcusuario, name='hcusuario'),    path('registrar-consulta/', views.registrar_consulta, name='registrar-consulta'),    path('registrar-consulta/', views.registrar_consulta, name='registrar-consulta'),
    
    # Órdenes médicas (paciente)
    #path('ordenes-medicas/', views.omusuario, name='omusuario'),
    #path('ordenes-medicamentos/', views.omeusuario, name='omeusuario'),
    path('orden/<int:id_orden>/pdf/', views.descargar_pdf_orden_paciente, name='descargar_pdf_orden_paciente'),
    
    # Turnos
    path('turnos/', views.turnosusuario, name='turnos_usuario'),
    
    # Páginas públicas
    path('preguntas-frecuentes/', views.preguntasfrecuentes, name='preguntas-frecuentes'),
    path('uso-del-sistema/', views.usosistema, name='usosistema'),
    path('buzon-sugerencias/', views.buzonsugerencias, name='buzon-sugerencias'),
    path('registrarse/', views.registro, name='registro'),
    path('contactanos/', views.contactanos, name='contactanos'),
]
