from django.urls import path
from . import views

app_name = 'rLaboratorio'

urlpatterns = [
    path('', views.inicio_laboratorista, name='inicio_laboratorista'),
    path('registrar-resultado/', views.registrar_resultado, name='registrar_resultado'),
]