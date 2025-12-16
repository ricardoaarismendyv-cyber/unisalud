from django.urls import path, include
from usuario import views as usuario_views
from administrativo import views as admin_views
from . import views


urlpatterns = [ 
    path('inicio/', views.inicio_prof_salud, name='inicio_prof_salud'),
    path('historia_clinica/', views.hc_prof_salud, name='hc_prof_salud'), # Se mantiene una sola ruta con este nombre
    path('historia-clinica/diligenciar/', views.diligenciar_hc, name='diligenciar_hc'), #formulario hc
    path('historia-clinica/ver-pdf/<int:consulta_id>/', views.ver_hc_pdf, name='ver_hc_pdf'),
    path('historia-clinica/generar-pdf/<int:consulta_id>/', views.generar_hc_pdf, name='generar_hc_pdf'),
    path('ordenes_medicas/', views.om_prof_salud, name='om_prof_salud'),
    path('ordenes_medicas/diligenciar_omedica/', views.diligenciar_omedica, name='diligenciar_omedica'),
    path('ordenes_medicas/ver-pdf/<int:orden_id>/', views.ver_omedica_pdf, name='ver_omedica_pdf'),
    path('ordenes_medicas/generar-pdf/<int:orden_id>/', views.generar_omedica_pdf, name='generar_omedica_pdf'),
    path('ordenes_medicamentos/', views.omed_prof_salud, name='omed_prof_salud'),
    path('ordenes_medicamentos/diligenciar/', views.diligenciar_omedicamentos, name='diligenciar_omedicamentos'),
    path('turnos/<int:id_profesional>/', views.consultas_prof_salud, name='consultas_prof_salud'),
    path('preguntas-frecuentes', views.preguntasfrecuentes_prof_salud, name='preguntas-frecuentes_prof_salud'),
    path('uso-del-sistema', views.usosistema_prof_salud, name='usosistema_prof_salud'),
    path('buzon-sugerencias', views.buzonsugerencias_prof_salud, name='buzonsugerencias_prof_salud'),
    path('contactanos', views.contactanos_prof_salud, name='contactanos_prof_salud')
]
