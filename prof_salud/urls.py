from django.urls import path, include
from usuario import views as usuario_views
from administrativo import views as admin_views
from . import views


app_name = 'prof_salud'
urlpatterns = [ 
    path('inicio/', views.inicio_prof_salud, name='inicio_prof_salud'),
    path('historia_clinica/', views.hc_prof_salud, name='hc_prof_salud'), # Se mantiene una sola ruta con este nombre
    path('historia_clinica/diligenciar/', views.diligenciar_hc, name='diligenciar_hc'), #formulario hc
    path('historia_clinica/ver-pdf/<int:consulta_id>/', views.ver_hc_pdf, name='ver_hc_pdf'),
    path('historia_clinica/generar-pdf/<int:consulta_id>/', views.generar_hc_pdf, name='generar_hc_pdf'),
    path('ordenes_medicas/', views.om_prof_salud, name='om_prof_salud'),
    path('ordenes_medicas/diligenciar_omedica/', views.diligenciar_omedica, name='diligenciar_omedica'),
    path('ordenes_medicas/ver-pdf/<int:orden_id>/', views.ver_omedica_pdf, name='ver_omedica_pdf'),
    path('ordenes_medicas/generar-pdf/<int:orden_id>/', views.generar_omedica_pdf, name='generar_omedica_pdf'),
    path('ordenes_medicamentos/', views.omed_prof_salud, name='omed_prof_salud'),
    path('ordenes_medicamentos/diligenciar/', views.diligenciar_omedicamentos, name='diligenciar_omedicamentos'),
    path('ordenes_medicamentos/ver-pdf/<int:orden_id>/', views.ver_omedicamentos_pdf, name='ver_omedicamentos_pdf'),
    path('ordenes_medicamentos/generar-pdf/<int:orden_id>/', views.generar_omedicamentos_pdf, name='generar_omedicamentos_pdf'),  
    path('consultas/', views.consultas_prof_salud, name='consultas_prof_salud'),
    path('turnos/', views.consultas_prof_salud, name='consultas_prof_salud'),
    path('preguntas_frecuentes', views.preguntasfrecuentes_prof_salud, name='preguntas_frecuentes_prof_salud'),
    path('uso_del_sistema', views.usosistema_prof_salud, name='usosistema_prof_salud'),
    path('buzon_sugerencias', views.buzonsugerencias_prof_salud, name='buzonsugerencias_prof_salud'),
    path('contactanos', views.contactanos_prof_salud, name='contactanos_prof_salud')
]
