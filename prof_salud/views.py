from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def inicio_prof_salud(request):
    # Obtener el perfil del usuario logueado
    try:
        perfil = PerfilUsuario.objects.select_related('id_rol').get(
            nombre_usuario=request.user.username
        )
        rol_nombre = perfil.id_rol.nombre_rol if perfil.id_rol else 'unknown'
    except PerfilUsuario.DoesNotExist:
        rol_nombre = 'unknown'
    
    # Contexto para la plantilla
    context = {
        'usuarios': request.user,
        'PERMISSIONS': {},  # Ajusta según tus permisos
        'rol_usuario': rol_nombre,
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

