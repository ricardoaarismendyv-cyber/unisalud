from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from usuario.models import OrdenMedica, EstadoOrden, Pacientes, DiagnosticoPaciente
from .forms import ConsultaForm, DiagnosticoForm, OrdenMedicaForm
from usuario.models import ProfesionalSalud, Usuarios, Roles, TipoIdentificacion, Genero, CentrosMedicos, Especialidades
from login.decorators import role_required
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
                profesional = ProfesionalSalud.objects.get(id_profesional=profesional_id)
                return render(request, 'paginas/inicio_prof_salud.html', {'profesional': profesional, 'roles': request.session.get('roles', [])})
        except ProfesionalSalud.DoesNotExist:
                messages.error(request, 'No se encontró el perfil del profesional de salud.')
                return redirect('login')

@role_required(allowed_roles=ALLOWED_PROF_ROLES)
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

#para historia clinica formulario
@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def registrar_consulta(request):
    """Vista para registrar consulta con diagnóstico integrado"""
    try:
        profesional_id = request.session.get('id_profesional')
        profesional = ProfesionalSalud.objects.get(id_profesional=profesional_id)
    except ProfesionalSalud.DoesNotExist:
        messages.error(request, 'No se encontró el perfil del profesional de salud.')
        return redirect('login')
    
    paciente = None
    
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        diagnostico_form = DiagnosticoForm(request.POST)
        
        numero_documento = request.POST.get('numero_documento')
        
        try:
            paciente = Pacientes.objects.get(numero_documento=numero_documento)
            
            if form.is_valid() and diagnostico_form.is_valid():
                # Guardar consulta
                consulta = form.save(commit=False)
                consulta.id_paciente = paciente
                consulta.id_profesional = profesional
                consulta.id_centro_medico = profesional.id_centro_medico
                consulta.fecha_atencion = timezone.now()
                consulta.creado_en = timezone.now()
                
                # Calcular IMC
                if consulta.peso and consulta.talla:
                    talla_metros = consulta.talla / 100
                    consulta.imc = round(float(consulta.peso) / (talla_metros ** 2), 2)
                
                consulta.save()
                
                # Guardar diagnóstico
                diagnostico = diagnostico_form.save(commit=False)
                diagnostico.id_consulta = consulta
                diagnostico.id_paciente = paciente
                diagnostico.fecha_diagnostico = timezone.now()
                diagnostico.save()
                
                messages.success(request, 'Consulta y diagnóstico guardados exitosamente.')
                return redirect('inicio-prof-salud')
            else:
                messages.error(request, 'Por favor corrija los errores en el formulario.')
                
        except Pacientes.DoesNotExist:
            messages.error(request, 'No se encontró un paciente con ese número de documento.')
    else:
        form = ConsultaForm()
        diagnostico_form = DiagnosticoForm()
    
    context = {
        'form': form,
        'diagnostico_form': diagnostico_form,
        'paciente': paciente,
        'profesional': profesional
    }
    
    return render(request, 'paginas/registrar-consulta.html', context)

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

# Vista para generar el PDF de una consulta específica para HC
@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def consulta_pdf(request, consulta_id):
    consulta = get_object_or_404(Consulta, pk=consulta_id)
    pdf_bytes = consulta.generate_pdf()
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=consulta_{consulta.id_consulta}.pdf'
    return response

@role_required(allowed_roles=['profesional_salud'])
def crear_orden_medica(request):
    """Vista para crear órdenes médicas."""
    try:
        profesional_id = request.session.get('id_profesional')
        profesional = ProfesionalSalud.objects.get(id_profesional=profesional_id)
    except ProfesionalSalud.DoesNotExist:
        messages.error(request, 'No se encontró tu perfil profesional.')
        return redirect('login')
    
    if request.method == 'POST':
        form = OrdenMedicaForm(request.POST, profesional=profesional)
        
        if form.is_valid():
            orden = form.save(commit=False)
            orden.id_profesional = profesional
            orden.id_centro_medico = profesional.id_centro_medico
            orden.fecha_emision = timezone.now()
            
            estado_pendiente, created = EstadoOrden.objects.get_or_create(
                nombre_estado_orden='pendiente'
            )
            orden.id_estado_orden = estado_pendiente
            orden.save()
            
            # NUEVO: Guardar PDF en PostgreSQL automáticamente
            orden.save_pdf_to_db()
            print(f"✅ PDF guardado en BD para orden #{orden.id_orden}")
            
            messages.success(request, f'Orden médica #{orden.id_orden} creada exitosamente.')
            return redirect('lista_ordenes_medicas')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = OrdenMedicaForm(profesional=profesional)
    
    context = {
        'form': form,
        'profesional': profesional,
    }
    return render(request, 'prof_salud/crear_orden_medica.html', context)

@role_required(allowed_roles=['profesional_salud'])
def lista_ordenes_medicas(request):
    """
    Lista las órdenes médicas creadas por el profesional.
    """
    try:
        profesional_id = request.session.get('id_profesional')
        profesional = ProfesionalSalud.objects.get(id_profesional=profesional_id)
    except ProfesionalSalud.DoesNotExist:
        messages.error(request, 'No se encontró tu perfil profesional.')
        return redirect('login')
    
    ordenes = OrdenMedica.objects.filter(
        id_profesional=profesional
    ).select_related(
        'id_paciente',
        'id_tipo_orden',
        'id_medicamento',
        'id_servicio',
        'id_estado_orden'
    ).order_by('-fecha_emision')[:100]  # Últimas 100
    
    context = {
        'ordenes': ordenes,
        'profesional': profesional,
    }
    return render(request, 'prof_salud/lista_orden_medicas.html', context)

@role_required(allowed_roles=['profesional_salud'])
def detalle_orden_medica(request, id_orden):
    """
    Vista para ver el detalle completo de una orden médica.
    Muestra toda la información: paciente, medicamento/servicio, indicaciones, etc.
    """
    try:
        profesional_id = request.session.get('id_profesional')
        profesional = ProfesionalSalud.objects.get(id_profesional=profesional_id)
    except ProfesionalSalud.DoesNotExist:
        messages.error(request, 'No se encontró tu perfil profesional.')
        return redirect('login')
    
    # Obtener la orden médica carga todas las relaciones FK en una sola consulta
    orden = get_object_or_404(
        OrdenMedica.objects.select_related(
            'id_paciente',
            'id_paciente__id_tipo_identificacion',
            'id_paciente__id_genero',
            'id_profesional',
            'id_profesional__id_especialidad',
            'id_tipo_orden',
            'id_medicamento',
            'id_servicio',
            'id_servicio__id_especialidad',
            'id_centro_medico',
            'id_estado_orden',
            'id_consulta'
        ),
        id_orden=id_orden
    )
    
    # Verificar que el profesional tenga permiso para ver esta orden
    # (solo puede ver órdenes de su centro médico o que él creó)
    if orden.id_profesional != profesional and orden.id_centro_medico != profesional.id_centro_medico:
        messages.error(request, 'No tienes permiso para ver esta orden.')
        return redirect('lista_ordenes_medicas')
    
    # Obtener diagnósticos relacionados si hay consulta vinculada
    diagnosticos = []
    if orden.id_consulta:
        diagnosticos = DiagnosticoPaciente.objects.filter(
            id_consulta=orden.id_consulta
        ).select_related('id_enfermedad')
    
    context = {
        'orden': orden,
        'profesional': profesional,
        'diagnosticos': diagnosticos,
        'es_medicamento': orden.id_tipo_orden.nombre_tipo.lower() == 'medicamentos',
        'es_examen': orden.id_tipo_orden.nombre_tipo.lower() in ['examenes', 'procedimientos'],
    }
    
    return render(request, 'prof_salud/detalle_orden_medica.html', context)

@role_required(allowed_roles=['profesional_salud'])
def generar_pdf_orden(request, id_orden):
    """
    Descarga el PDF de una orden médica desde PostgreSQL.
    """
    try:
        profesional_id = request.session.get('id_profesional')
        profesional = ProfesionalSalud.objects.get(id_profesional=profesional_id)
    except ProfesionalSalud.DoesNotExist:
        messages.error(request, 'No se encontró tu perfil profesional.')
        return redirect('login')
    
    orden = get_object_or_404(OrdenMedica, id_orden=id_orden)
    
    # Verificar permisos
    if orden.id_profesional != profesional and orden.id_centro_medico != profesional.id_centro_medico:
        messages.error(request, 'No tienes permiso para ver esta orden.')
        return redirect('lista_ordenes_medicas')
    
    # Obtener PDF desde PostgreSQL (columna BYTEA)
    pdf_bytes = orden.get_pdf_from_db()
    
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="orden_{orden.id_orden}.pdf"'
    return response
