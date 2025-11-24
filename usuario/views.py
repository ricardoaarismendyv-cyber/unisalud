from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Turno
import uuid
from datetime import timedelta
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

# views.py
import qrcode
import base64
from io import BytesIO
import uuid
from django.shortcuts import render
from .models import Turno  # si quieres guardarlo en BD

import random

def turnosusuario(request):
    turno = random.randint(1000, 9999)  # Número entre 1000 y 9999

    qr = qrcode.make(str(turno))
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'paginas/turnos-usuario.html', {
        "turno": turno,
        "qr_base64": qr_base64
    })



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

