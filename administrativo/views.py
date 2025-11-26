from django.shortcuts import render, redirect
import qrcode
import base64
from io import BytesIO
import uuid
from django.shortcuts import render
from usuario.models import Turnos
import string

# Create your views here.

def login_admin(request):
    return render(request, 'paginas/login_admin.html')

def inicio_admin(request):
    return render(request, 'paginas/inicio_admin.html')

def registro_admin(request):
    return render(request, 'paginas/registro_admin.html')

def hc_admin(request):
    return render(request, 'paginas/hc_admin.html')

def buzonsugerencias_admin(request):
    return render(request, 'paginas/buzon-sugerencias_admin.html')

def gestion_admin(request):
    return render(request, 'paginas/gestion_admin.html')

def hc_admin(request):
    return render(request, 'paginas/hc_admin.html')

def om_admin(request):
    return render(request, 'paginas/om_admin.html')

def omed_admin(request):
    return render(request, 'paginas/omed_admin.html')

def preguntasfrecuentes_admin(request):
    return render(request, 'paginas/preguntas-frecuentes_admin.html')

def usosistema_admin(request):
    return render(request, 'paginas/uso-sistema_admin.html')

def contactanos_admin(request):
    return render(request, 'paginas/contactanos_admin.html')


# views.py# si quieres guardarlo en BD

def turnos_admin(request):
    # Generar el siguiente turno ordenado
    turno_obj = generar_turno()
    turno = f"{turno_obj.letra}{turno_obj.numero:03d}"

    # Crear QR
    qr = qrcode.make(turno)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'paginas/turnos-usuario.html', {
        "turno": turno,
        "qr_base64": qr_base64
    })

# utils.py
import string
from usuario.models import Turnos

def generar_turno():
    # Si no hay turnos previos, comenzar en A001
    ultimo = Turnos.objects.order_by('-id').first()

    if not ultimo:
        return Turnos.objects.create(letra="A", numero=1)

    letra = ultimo.letra
    numero = ultimo.numero

    # Si el número llega a 999 → pasar a siguiente letra
    if numero >= 999:
        letras = list(string.ascii_uppercase)
        pos = letras.index(letra)

        # Si llega a Z999 → reiniciar A001
        if pos == len(letras) - 1:
            letra = "A"
        else:
            letra = letras[pos + 1]

        numero = 1
    else:
        numero += 1

    return Turnos.objects.create(letra=letra, numero=numero)
