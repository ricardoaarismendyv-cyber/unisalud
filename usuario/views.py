from django.shortcuts import render, redirect
from login.decorators import role_required
from .models import pacientes
from django.contrib import messages

@role_required(allowed_roles=['paciente'])
def inicio_usuario(request):
    try:
        # Obtener el ID del paciente desde la sesión
        paciente_id = request.session.get('id_paciente')
        paciente = pacientes.objects.get(id_paciente=paciente_id)
        return render(request, 'paginas/inicio-usuario.html', {'paciente': paciente})
    except pacientes.DoesNotExist:
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

# Esta vista podría ser pública o requerir login dependiendo de tu lógica de negocio
def buzonsugerencias(request):
    return render(request, 'paginas/buzon-sugerencias.html')

# La vista de registro debe ser pública
def registro(request):
    return render(request, 'paginas/registro.html')

# La vista de contacto debe ser pública
def contactanos(request):
    return render(request, 'paginas/contactanos.html')
