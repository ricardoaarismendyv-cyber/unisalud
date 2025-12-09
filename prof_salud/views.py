from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from usuario.models import ProfesionalSalud, Usuarios, Roles, TipoIdentificacion, Genero, CentrosMedicos, Especialidades, Turnos
from login.decorators import role_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


ALLOWED_PROF_ROLES = ['profesional_salud', 'laboratorista', 'recepcionista', 'admin_centro_medico']

@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def inicio_prof_salud(request):
        try:
                # Obtener el ID del profesional desde la sesión y buscar el objeto
                profesional_id = request.session.get('id_profesional')
                if not profesional_id:
                        messages.error(request, 'No se encontró un perfil de profesional de salud en su sesión.')
                        return redirect('login')
                request.session['active_role'] = 'profesional_salud' # <--- AÑADIR ESTA LÍNEA
                profesional = ProfesionalSalud.objects.get(id_profesional=profesional_id)
                return render(request, 'paginas/inicio_prof_salud.html', {'profesional': profesional, 'roles': request.session.get('roles', [])})
        except ProfesionalSalud.DoesNotExist:
                messages.error(request, 'No se encontró el perfil del profesional de salud.')
                return redirect('login')

@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def hc_prof_salud(request):
    return render(request, 'paginas/hc_prof_salud.html') #Vista de Historia Clínica para el profesional de salud

@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def om_prof_salud(request):
    return render(request, 'paginas/om_prof_salud.html') #Vista de Orden Médica para el profesional de salud

@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def omed_prof_salud(request):
    return render(request, 'paginas/omed_prof_salud.html') #Vista de Orden de Medicamentos para el profesional de salud.

@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def consultas_prof_salud(request):
    return render(request, 'paginas/consultas_prof_salud.html') #Vista de Turnos/Agendamiento para el profesional de salud

@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def preguntasfrecuentes_prof_salud(request):
    return render(request, 'paginas/preguntas-frecuentes_prof_salud.html')

@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def usosistema_prof_salud(request):
    return render(request, 'paginas/uso-sistema_prof_salud.html')

@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def buzonsugerencias_prof_salud(request):
    return render(request, 'paginas/buzon-sugerencias_prof_salud.html')

@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def contactanos_prof_salud(request):
    return render(request, 'paginas/contactanos_prof_salud.html')

# Esta vista es para registrar un nuevo profesional, podría ser pública o restringida a un admin.
# Por ahora, la dejamos sin decorador.
def registro_prof_salud(request):
    context = {
        'tipos_identificacion': TipoIdentificacion.objects.all(),
        'generos': Genero.objects.all(),
    }
    return render(request, 'paginas/registro_prof_salud.html', context)


def consultas_prof_salud(request):
    # Obtener id del profesional desde la sesión
    id_prof = request.session.get("id_profesional")

    if not id_prof:
        return HttpResponse("No se encontró un profesional en sesión")

    # Obtener profesional
    profesional = ProfesionalSalud.objects.get(id_profesional=id_prof)

    # Obtener turnos asignados a ese profesional
    turnos = Turnos.objects.filter(id_profesional=id_prof).order_by('fecha', 'hora')

    context = {
        "profesional": profesional,
        "turnos": turnos,
    }

    return render(request, 'paginas/consultas_prof_salud.html', context)