from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from usuario.models import Pacientes, Consulta, ProfesionalSalud, CentrosMedicos
from .forms import ConsultaForm, DiagnosticoForm

def inicio_prof_salud(request):
        # Verificar si el usuario es un profesional de la salud
        if request.session.get('nombre_rol') not in ['profesional_salud', 'laboratorista', 'recepcionista', 'admin_centro_medico']:
                messages.error(request, 'Acceso no autorizado.')
                return redirect('login')

        try:
                # Obtener el ID del profesional desde la sesión y buscar el objeto
                profesional_id = request.session.get('id_profesional')
                profesional = ProfesionalSalud.objects.get(id_profesional=profesional_id)
                return render(request, 'paginas/inicio_prof_salud.html', {'profesional': profesional})
        except ProfesionalSalud.DoesNotExist:
                messages.error(request, 'No se encontró el perfil del profesional de salud.')
                return redirect('login')

@login_required
def hc_prof_salud(request):
    """Vista de Historia Clínica para el profesional de salud"""
    
    # Obtener el profesional de salud logueado
    try:
        profesional = ProfesionalSalud.objects.get(usuario=request.user)
    except ProfesionalSalud.DoesNotExist:
        messages.error(request, 'No se encontró el perfil de profesional de salud.')
        return redirect('inicio_prof_salud')
    
    paciente = None
    form = ConsultaForm(request.POST or None)
    
    # Búsqueda de paciente
    if request.method == 'POST' and 'buscar_paciente' in request.POST:
        numero_documento = request.POST.get('numero_documento')
        try:
            paciente = Pacientes.objects.get(numero_documento=numero_documento)
            messages.success(request, f'Paciente encontrado: {paciente.nombre1} {paciente.apellido1}')
        except Pacientes.DoesNotExist:
            messages.error(request, 'No se encontró un paciente con ese número de documento.')
    
    # Guardar consulta
    if request.method == 'POST' and 'guardar_consulta' in request.POST:
        numero_documento = request.POST.get('numero_documento')
        try:
            paciente = Pacientes.objects.get(numero_documento=numero_documento)
            
            if form.is_valid():
                consulta = form.save(commit=False)
                consulta.id_paciente = paciente
                consulta.id_profesional = profesional
                consulta.id_centro_medico = profesional.id_centro_medico
                consulta.fecha_atencion = timezone.now()
                consulta.creado_en = timezone.now()
                
                # Calcular IMC si hay peso y talla
                if consulta.peso and consulta.talla:
                    talla_metros = consulta.talla / 100
                    consulta.imc = round(float(consulta.peso) / (talla_metros ** 2), 2)
                
                consulta.save()
                messages.success(request, 'Historia clínica guardada exitosamente.')
                return redirect('hc_prof_salud')
            else:
                messages.error(request, 'Por favor corrija los errores en el formulario.')
        except Pacientes.DoesNotExist:
            messages.error(request, 'Debe buscar un paciente primero.')
    
    context = {
        'form': form,
        'paciente': paciente,
        'profesional': profesional
    }
    
    return render(request, 'paginas/hc_prof_salud.html', context)

def om_prof_salud(request):
    return render(request, 'paginas/om_prof_salud.html') #Vista de Orden Médica para el profesional de salud

def omed_prof_salud(request):
    return render(request, 'paginas/omed_prof_salud.html') #Vista de Orden de Medicamentos para el profesional de salud.

def consultas_prof_salud(request):
    return render(request, 'paginas/consultas_prof_salud.html') #Vista de Turnos/Agendamiento para el profesional de salud

def preguntasfrecuentes_prof_salud(request):
    return render(request, 'paginas/preguntas-frecuentes_prof_salud.html')

def usosistema_prof_salud(request):
    return render(request, 'paginas/uso-sistema_prof_salud.html')

def buzonsugerencias_prof_salud(request):
    return render(request, 'paginas/buzon-sugerencias_prof_salud.html')

def contactanos_prof_salud(request):
    return render(request, 'paginas/contactanos_prof_salud.html')

def registro_prof_salud(request):
    context = {
        'tipos_identificacion': TipoIdentificacion.objects.all(),
        'generos': Genero.objects.all(),
    }
    return render(request, 'paginas/registro_prof_salud.html', context)
