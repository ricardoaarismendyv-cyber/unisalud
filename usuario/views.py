from django.shortcuts import render, redirect
from login.decorators import role_required
from .models import Pacientes, Consulta, OrdenMedica, ResultadosLaboratorio
from django.urls import reverse
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
    paciente_id = request.session.get('id_paciente')
    # Obtenemos todas las consultas del paciente, ordenadas de más reciente a más antigua
    historial_consultas = Consulta.objects.filter(id_paciente_id=paciente_id, estado='Atendido').order_by('-fecha_atencion')
    # La última consulta es el primer elemento de la lista
    ultima_consulta = historial_consultas.first()
    
    return render(request, 'paginas/historia-clinica-usuario.html', {
        'ultima_consulta': ultima_consulta,
        'historial': historial_consultas
    })

@role_required(allowed_roles=['paciente'])
def ver_hc_usuario_pdf(request, consulta_id):
    # Construir la URL hacia el PDF generado en prof_salud
    pdf_url = reverse('prof_salud:generar_hc_pdf', args=[consulta_id])

    # Renderizar plantilla con iframe (ruta estandarizada)
    return render(request, 'paginas/ver_hc_usuario_pdf.html', {
        'pdf_url': pdf_url,
        'consulta_id': consulta_id
    })

@role_required(allowed_roles=['paciente'])
def omusuario(request):
    paciente_id = request.session.get('id_paciente')
    # Obtenemos todas las órdenes de servicios agrupadas por lote
    ordenes = OrdenMedica.objects.filter(
        id_paciente_id=paciente_id,
        id_servicio__isnull=False
    ).order_by('id_lote', '-fecha_emision').distinct('id_lote')
    # La última orden es el primer elemento
    ultima_orden = ordenes.first()
    
    # Obtenemos también los resultados de laboratorio del paciente
    historial_resultados = ResultadosLaboratorio.objects.filter(
        id_paciente_id=paciente_id
    ).order_by('-fecha_registro_resultado')
    ultimo_resultado = historial_resultados.first()
    
    return render(request, 'paginas/orden-medica-usuario.html', {
        'ultima_orden': ultima_orden,
        'ordenes': ordenes, # Pasamos el historial completo a la plantilla
        'ultimo_resultado': ultimo_resultado,
        'historial_resultados': historial_resultados
    })

@role_required(allowed_roles=['paciente'])
def ver_orden_medica_usuario_pdf(request, orden_id):
    # Construir la URL hacia el PDF generado en prof_salud
    pdf_url = reverse('prof_salud:generar_omedica_pdf', args=[orden_id])

    # Renderizar plantilla con iframe (ruta estandarizada)
    return render(request, 'paginas/ver_orden_medica_usuario_pdf.html', {
        'pdf_url': pdf_url,
        'orden_id': orden_id
    })

@role_required(allowed_roles=['paciente'])
def omeusuario(request):
    paciente_id = request.session.get('id_paciente')
    # Obtenemos todas las órdenes de medicamentos agrupadas por lote
    ordenes = OrdenMedica.objects.filter(
        id_paciente_id=paciente_id,
        id_medicamento__isnull=False
    ).order_by('id_lote', '-fecha_emision').distinct('id_lote')
    # La última orden es el primer elemento
    ultima_orden = ordenes.first()
    
    return render(request, 'paginas/orden-medicamentos-usuario.html', {
        'ultima_orden': ultima_orden,
        'ordenes': ordenes
    })


@role_required(allowed_roles=['paciente'])
def ver_orden_medicamentos_usuario_pdf(request, orden_id):
    # Construir la URL hacia el PDF generado en prof_salud
    pdf_url = reverse('prof_salud:generar_omedicamentos_pdf', args=[orden_id])

    # Renderizar plantilla con iframe (ruta estandarizada)
    return render(request, 'paginas/ver_orden_medicamentos_usuario_pdf.html', {
        'pdf_url': pdf_url,
        'orden_id': orden_id
    })

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
