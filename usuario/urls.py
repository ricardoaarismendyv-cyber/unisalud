from django.urls import path
from . import views


urlpatterns = [
    # Las URLs de login y logout son manejadas por la app 'login'
    path('', views.inicio_usuario, name='inicio-usuario'),
    path('historia-clinica', views.hcusuario, name='hcusuario'),
    path('historia-clinica/ver-pdf/<int:consulta_id>/', views.ver_hc_usuario_pdf, name='ver_hc_usuario_pdf'),
    path('ordenes-medicas', views.omusuario, name='omusuario'),
    path('ordenes-medicas/ver-pdf/<int:orden_id>/', views.ver_orden_medica_usuario_pdf, name='ver_orden_medica_usuario_pdf'),
    path('ordenes-medicamentos', views.omeusuario, name='omeusuario'),
    path('ordenes-medicamentos/ver-pdf/<int:orden_id>/', views.ver_orden_medicamentos_usuario_pdf, name='ver_orden_medicamentos_usuario_pdf'),
    path('turnos', views.turnosusuario, name='turnos-usuario'),
    path('preguntas-frecuentes', views.preguntasfrecuentes, name='preguntas-frecuentes'),
    path('uso-del-sistema', views.usosistema, name='usosistema'),
    path('buzon-sugerencias', views.buzonsugerencias, name='buzonsugerencias'),
    path('contactanos', views.contactanos, name='contactanos'),
]
