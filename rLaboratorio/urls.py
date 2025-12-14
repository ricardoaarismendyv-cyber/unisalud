from django.urls import path
from . import views

app_name = 'rLaboratorio'

urlpatterns = [
    path('', views.inicio_laboratorista, name='inicio_laboratorista'),
    path('registrar-resultado/', views.registrar_resultado, name='registrar_resultado'),
    path('ver-resultado/<int:resultado_id>/', views.ver_resultado_pdf, name='ver_resultado_pdf'),
    path('generar-resultado-pdf/<int:resultado_id>/', views.generar_resultado_pdf_vista, name='generar_resultado_pdf_vista'),
]