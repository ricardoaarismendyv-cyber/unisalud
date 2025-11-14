from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from usuarios.models import roles_usuario
# Create your views here.

@login_required

def inicio_prof_salud(request):

    roles_usuario = roles.objects.filter(id_usuario=request.user.id)

    PERMISSIONS = {
        usuario.nombre_rol: 0,
    }

    for roles_usuario in roles_usuario:
        roles = roles_usuario.roles.nombre_rol
        for module in permissions.keys():
            current_permission = getattr(roles_usuario, module)
            if current_permission > PERMISSIONS[module]:
                PERMISSIONS[module] = current_permission
    
    context = {
        'usuarios' : request.user,
        'PERMISSIONS' : PERMISSIONS
        'roles_usuario' : [ur.roles.rol_nombre for ur in roles_usuario],
    }

    return render(request, 'paginas/inicio_prof_salud.html', context) #Vista de inicio para el profesional de salud

def hc_prof_salud(request):
    return render(request, 'paginas/hc_prof_salud.html') #Vista de Historia Clínica para el profesional de salud

def om_prof_salud(request):
    return render(request, 'paginas/om_prof_salud.html') #Vista de Orden Médica para el profesional de salud

def omed_prof_salud(request):
    return render(request, 'paginas/omed_prof_salud.html') #Vista de Orden de Medicamentos para el profesional de salud.

def consultas_prof_salud(request):
    return render(request, 'paginas/consultas_prof_salud.html') #Vista de Turnos/Agendamiento para el profesional de salud

def registro_prof_salud(request):
    return render(request, 'paginas/registro_prof_salud.html') #Vista para el formulario de registro de nuevos usuarios.   

def preguntasfrecuentes_prof_salud(request):
    return render(request, 'paginas/preguntas-frecuentes_prof_salud.html')

def usosistema_prof_salud(request):
    return render(request, 'paginas/uso-sistema_prof_salud.html')

def buzonsugerencias_prof_salud(request):
    return render(request, 'paginas/buzon-sugerencias_prof_salud.html')

def contactanos_prof_salud(request):
    return render(request, 'paginas/contactanos_prof_salud.html')

