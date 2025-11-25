from django.shortcuts import render, redirect
from login.decorators import role_required
from django.contrib import messages

# Create your views here.
ALLOWED_ADMIN_ROLES = ['admin_centro_medico']

def login_admin(request):
    return render(request, 'paginas/login_admin.html')

@role_required(allowed_roles=ALLOWED_ADMIN_ROLES)
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

def turnos_admin(request):
    return render(request, 'paginas/turnos_admin.html')
    request.session['active_role'] = 'admin_centro_medico' # <--- AÑADIR ESTA LÍNEA
    # Aquí puedes añadir lógica para buscar el perfil del admin si es necesario
    return render(request, 'paginas/inicio_admin.html', {'roles': request.session.get('roles', [])})