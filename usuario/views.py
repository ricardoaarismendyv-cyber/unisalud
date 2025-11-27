from django.shortcuts import render, redirect
from login.decorators import role_required
from .models import Pacientes, Usuarios, Roles, TipoIdentificacion, Genero
from django.contrib import messages

@role_required(allowed_roles=['paciente'])
def inicio_usuario(request):
    try:
        paciente_id = request.session.get('id_paciente')
        if not paciente_id:
            # Si no hay id_paciente en la sesión, es un error de acceso.
            messages.error(request, 'No tienes permiso para acceder a esta página. Se requiere un perfil de paciente.')
            return redirect('login')
        request.session['active_role'] = 'paciente' # <--- AÑADIR ESTA LÍNEA
        paciente = Pacientes.objects.get(id_paciente=paciente_id)
        return render(request, 'paginas/inicio-usuario.html', {'paciente': paciente, 'roles': request.session.get('roles', [])})
    except Pacientes.DoesNotExist:
        messages.error(request, 'No se encontró el perfil del paciente.')
        return redirect('login')

@role_required(allowed_roles=['paciente'])
def hcusuario(request):
    return render(request, 'paginas/historia-clinica-usuario.html')

@role_required(allowed_roles=['paciente'])
def omusuario(request):
    return render(request, 'paginas/orden-medica-usuario.html')

@role_required(allowed_roles=['paciente'])
def omeusuario(request):
    return render(request, 'paginas/orden-medicamentos-usuario.html')

@role_required(allowed_roles=['paciente'])
def turnosusuario(request):
    return render(request, 'paginas/turnos-usuario.html')

# Las siguientes vistas pueden ser públicas, no requieren login
def preguntasfrecuentes(request):
    return render(request, 'paginas/preguntas-frecuentes.html')

def usosistema(request):
    return render(request, 'paginas/uso-sistema.html')

def buzonsugerencias(request):
    return render(request, 'paginas/buzon-sugerencias.html')

def contactanos(request):
    return render(request, 'paginas/contactanos.html')
