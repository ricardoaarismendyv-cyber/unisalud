from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.

def loginus(request):
    return render(request, 'paginas/login-us.html' )


def iniciousuario(request):
    return render(request, 'paginas/inicio-usuario.html')

def hcusuario(request):
    return render(request, 'paginas/historia-clinica-usuario.html')

def omusuario(request):
    return render(request, 'paginas/orden-medica-usuario.html')

def omeusuario(request):
    return render(request, 'paginas/orden-medicamentos-usuario.html')

def turnosusuario(request):
    return render(request, 'paginas/turnos-usuario.html')

def preguntasfrecuentes(request):
    return render(request, 'paginas/preguntas-frecuentes.html')

def usosistema(request):
    return render(request, 'paginas/uso-sistema.html')

def buzonsugerencias(request):
    return render(request, 'paginas/buzon-sugerencias.html')

def registro(request):
    return render(request, 'paginas/registro.html')

def contactanos(request):
    return render(request, 'paginas/contactanos.html')


def pacientes(request): 
    pacientes=Pacientes.objects.all()
    #print(estudiantes)
    return render(request, "estudiantes/materias.html", {'pacientes':pacientes}) 