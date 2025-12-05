from django.urls import path, include
from usuario import views as usuario_views
from administrativo import views as admin_views
from . import views


urlpatterns = [ 
    path('inicio/', views.inicio_prof_salud, name='inicio_prof_salud'),
    path('paciente/logout_prof_salud/historia_clinica/', views.hc_prof_salud, name='hc_prof_salud'),
    path('historia_clinica/', views.hc_prof_salud, name='hc_prof_salud'),
    path('historia-clinica/diligenciar/', views.diligenciar_hc, name='diligenciar_hc'), #formulario hc
    path('historia-clinica/ver-pdf/<int:consulta_id>/', views.ver_hc_pdf, name='ver_hc_pdf'),
    path('historia-clinica/generar-pdf/<int:consulta_id>/', views.generar_hc_pdf, name='generar_hc_pdf'),
    path('ordenes_medicas/', views.om_prof_salud, name='om_prof_salud'),
    path('ordenes_medicas/diligenciar/', views.diligenciar_orden_medica, name='diligenciar_orden_medica'),
    path('ordenes_medicamentos/', views.omed_prof_salud, name='omed_prof_salud'),
    path('turnos/', views.consultas_prof_salud, name='consultas_prof_salud'),
    path('preguntas-frecuentes', views.preguntasfrecuentes_prof_salud, name='preguntas-frecuentes_prof_salud'),
    path('uso-del-sistema', views.usosistema_prof_salud, name='usosistema_prof_salud'),
    path('buzon-sugerencias', views.buzonsugerencias_prof_salud, name='buzonsugerencias_prof_salud'),
    path('contactanos', views.contactanos_prof_salud, name='contactanos_prof_salud')
]
