# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio_turnero, name="inicio-turnero"),
    path("turnero/gestionar/", views.gestionar_turnero, name="gestionar_turnos"),
    path('llamar/<int:id_turno>/', views.llamar_turno, name="llamar-turno"),
    path('cerrar/<int:id_turno>/', views.cerrar_turno, name="cerrar-turno"),
    path('pantalla/', views.pantalla_turnos, name='pantalla_turnos'),
    path("turnos/volver-llamar/<int:id_turno>/", views.volver_llamar, name="volver-llamar"),
]
