from django.shortcuts import render, redirect
from django.contrib import messages
from usuario.models import ProfesionalSalud, Usuarios, Roles, TipoIdentificacion, Genero, CentrosMedicos, Especialidades, DiagnosticoPaciente, AntecedentesPaciente, Enfermedades, Consulta, OrdenMedica, Servicios, EstadoOrden, TipoOrden, Medicamentos, Pacientes
from login.decorators import role_required
from .forms import ConsultaForm, DiagnosticoFormSet, AntecedenteFormSet, OrdenMedicaForm, serviciosFormSet, OrdenMedicamentoForm, MedicamentoFormSet
from django.utils import timezone
import json
from django.http import HttpResponse
from django.template.loader import get_template #obtener o descargar una plantilla de diseño web
from xhtml2pdf import pisa #conversión real que realiza el trabajo de transformar el contenido HTML y CSS en el formato PDF.
import qrcode # Para generar códigos QR
import uuid # Para generar el id_lote
from io import BytesIO #generar un archivo (como un PDF o una imagen) y enviarlo inmediatamente a un usuario a través de una API web, sin tocar el sistema de archivos del servidor.
from django.urls import reverse # <--- AÑADIR ESTA LÍNEA
from django.core.serializers.json import DjangoJSONEncoder
import base64
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_sameorigin

ALLOWED_PROF_ROLES = ['profesional_salud', 'laboratorista', 'recepcionista', 'admin_centro_medico']

@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def inicio_prof_salud(request):
        try:
                # Obtener el ID del profesional desde la sesión y buscar el objeto
                profesional_id = request.session.get('id_profesional')
                if not profesional_id:
                        messages.error(request, 'No se encontró un perfil de profesional de salud en su sesión.')
                        return redirect('login')
                #  asegura que el rol activo se mantenga consistente a lo largo de la sesión del usuario, especialmente cuando navega entre diferentes perfiles si tiene más de uno.
                if 'active_role' not in request.session:
                        request.session['active_role'] = 'profesional_salud'
                profesional = ProfesionalSalud.objects.get(id_profesional=profesional_id)
                return render(request, 'paginas/inicio_prof_salud.html', {'profesional': profesional, 'roles': request.session.get('roles', [])})
        except ProfesionalSalud.DoesNotExist:
                messages.error(request, 'No se encontró el perfil del profesional de salud.')
                return redirect('login')

@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def hc_prof_salud(request):
    """
    Vista de Historia Clínica para el profesional de salud.
    Muestra la última consulta registrada por el profesional.
    """
    ultima_consulta = None
    historial_paciente = None
    try:
        profesional_id = request.session.get('id_profesional')
        if profesional_id:
            profesional = ProfesionalSalud.objects.get(id_profesional=profesional_id)
            # Se busca la última consulta atendida por este profesional
            ultima_consulta = Consulta.objects.filter(id_profesional=profesional, estado='Atendido').order_by('-fecha_atencion').first()

            # Si encontramos una última consulta, buscamos el historial de ese paciente
            if ultima_consulta:
                paciente = ultima_consulta.id_paciente
                # Obtenemos las últimas 5 consultas de ese paciente, ordenadas por fecha
                historial_paciente = Consulta.objects.filter(id_paciente=paciente, estado='Atendido').order_by('-fecha_atencion')[:5]

    except ProfesionalSalud.DoesNotExist:
        messages.error(request, 'No se pudo encontrar el perfil del profesional.')
    except Exception as e:
        messages.error(request, f'Ocurrió un error inesperado: {e}')

    return render(request, 'paginas/hc_prof_salud.html', {'ultima_consulta': ultima_consulta, 'historial_paciente': historial_paciente})

@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def om_prof_salud(request):
    """
    Vista de Orden Médica para el profesional de salud.
    Muestra la última orden médica registrada por el profesional.
    """
    ultima_orden_medica = None
    historial_ordenes_medicas = None
    try:
        profesional_id = request.session.get('id_profesional')
        if profesional_id:
            profesional = ProfesionalSalud.objects.get(id_profesional=profesional_id)
            # Se busca la última OrdenMedica atendida por este profesional
            ultima_orden_medica = OrdenMedica.objects.filter(id_profesional=profesional).order_by('-fecha_emision').first()

            # Si encontramos una última orden médica, buscamos el historial de ese paciente
            if ultima_orden_medica:
                paciente = ultima_orden_medica.id_paciente
                # Obtenemos las últimas órdenes médicas de ese paciente, ordenadas por fecha
                historial_ordenes_medicas = OrdenMedica.objects.filter(id_paciente=paciente).order_by('-fecha_emision')[:5] # Puedes ajustar el límite

    except ProfesionalSalud.DoesNotExist:
        messages.error(request, 'No se pudo encontrar el perfil del profesional.')
    except Exception as e:
        messages.error(request, f'Ocurrió un error inesperado: {e}')

    return render(request, 'paginas/om_prof_salud.html', {'ultima_orden_medica': ultima_orden_medica, 'historial_ordenes_medicas': historial_ordenes_medicas})

@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def omed_prof_salud(request):
    """
    Vista de Órdenes de Medicamentos para el profesional de salud.
    Muestra la última orden de medicamentos registrada por el profesional y el historial del paciente.
    """
    ultima_orden_medicamentos = None
    historial_ordenes_medicamentos = None
    try:
        profesional_id = request.session.get('id_profesional')
        if profesional_id:
            profesional = ProfesionalSalud.objects.get(id_profesional=profesional_id)
            # Buscamos la última OrdenMedicamentos atendida por este profesional
            ultima_orden_medicamentos = OrdenMedica.objects.filter(
                id_profesional=profesional, 
                id_medicamento__isnull=False
            ).order_by('-fecha_emision').first()

            # Si encontramos una última orden médicamentos, buscamos el historial de ese paciente
            if ultima_orden_medicamentos:
                paciente = ultima_orden_medicamentos.id_paciente
                # Obtenemos las últimas 5 órdenes de medicamentos de ese paciente.
                historial_ordenes_medicamentos = OrdenMedica.objects.filter(
                    id_paciente=paciente, id_medicamento__isnull=False
                ).order_by('-fecha_emision')[:5]

    except ProfesionalSalud.DoesNotExist:
        messages.error(request, 'No se pudo encontrar el perfil del profesional.')
    except Exception as e:
        messages.error(request, f'Ocurrió un error inesperado: {e}')

    return render(request, 'paginas/omed_prof_salud.html', {'ultima_orden_medicamentos': ultima_orden_medicamentos, 'historial_ordenes_medicamentos': historial_ordenes_medicamentos})

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

@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def diligenciar_hc(request):
    profesional_id = request.session.get('id_profesional')
    if not profesional_id:
        messages.error(request, 'No se pudo identificar al profesional. Por favor, inicie sesión de nuevo.')
        return redirect('login')

    profesional = ProfesionalSalud.objects.get(id_profesional=profesional_id)

    if request.method == 'POST':
        consulta_form = ConsultaForm(request.POST)
        diagnostico_formset = DiagnosticoFormSet(request.POST, prefix='diagnosticos')
        antecedente_formset = AntecedenteFormSet(request.POST, prefix='antecedentes')

        if consulta_form.is_valid() and diagnostico_formset.is_valid() and antecedente_formset.is_valid():
            try:
                nueva_consulta = consulta_form.save(commit=False)
                
                # Asignar los datos que no vienen del formulario
                nueva_consulta.id_profesional = profesional
                nueva_consulta.id_centro_medico = profesional.id_centro_medico
                nueva_consulta.fecha_programada = timezone.now() # O la fecha de la cita real
                nueva_consulta.fecha_atencion = timezone.now()
                nueva_consulta.estado = 'Atendido'
                nueva_consulta.save()

                # Guardar los diagnósticos del formset
                for form in diagnostico_formset:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        # El ID de la enfermedad ahora viene del campo oculto 'id_enfermedad'
                        enfermedad_obj = form.cleaned_data.get('id_enfermedad')
                        DiagnosticoPaciente.objects.create(
                            id_consulta=nueva_consulta,
                            id_enfermedad=enfermedad_obj,
                            # Usamos .get() para evitar un KeyError si el campo está vacío
                            tipo_diagnostico=form.cleaned_data.get('tipo_diagnostico'),
                            notas=form.cleaned_data.get('notas', ''),
                            fecha_registro=timezone.now()
                        )

                # Guardar los antecedentes del formset
                for form in antecedente_formset:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        antecedente = form.save(commit=False)
                        antecedente.id_paciente = nueva_consulta.id_paciente # Usamos el paciente de la consulta
                        antecedente.fecha_registro = timezone.now().date() # Extraer solo la fecha
                        antecedente.save()

                messages.success(request, f'Historia clínica para el paciente {nueva_consulta.id_paciente} guardada con éxito.')
                return redirect('prof_salud:ver_hc_pdf', consulta_id=nueva_consulta.id_consulta)
            except Exception as e:
                messages.error(request, f'Ocurrió un error al guardar la historia clínica: {e}')
    else:
        consulta_form = ConsultaForm()
        diagnostico_formset = DiagnosticoFormSet(prefix='diagnosticos', initial=[{}]) # Inicia con un form vacío
        antecedente_formset = AntecedenteFormSet(prefix='antecedentes', initial=[{}]) # Inicia con un form vacío

    # Preparar datos de enfermedades para JavaScript
    enfermedades_data = {
        e.id_enfermedad: {
            'categoria': e.categoria_grupom,
            'grupo': e.grupo_mortalidad
        } for e in Enfermedades.objects.all()
    }
    enfermedades_json = json.dumps(enfermedades_data)

    return render(request, 'paginas/diligenciar_hc.html', {
        'form': consulta_form, 
        'diagnostico_formset': diagnostico_formset,
        'antecedente_formset': antecedente_formset,
        'enfermedades_json': enfermedades_json
    })

def render_to_pdf(template_src, context_dict={}):
    """
    Función auxiliar para renderizar una plantilla HTML a un objeto PDF.
    """
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        # Devolvemos solo los bytes del PDF, no la respuesta HTTP completa
        return result.getvalue()
    return None

@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def ver_hc_pdf(request, consulta_id):
    """
    Muestra una página con el PDF de la HC incrustado y opciones para descargar o volver.
    """
    try:
        # Verificamos que la consulta exista para evitar errores
        consulta = Consulta.objects.get(id_consulta=consulta_id)
        return render(request, 'paginas/ver_hc_pdf.html', {'consulta': consulta})
    except Consulta.DoesNotExist:
        messages.error(request, 'La consulta solicitada no existe.')
        return redirect('hc_prof_salud')

@role_required(allowed_roles=ALLOWED_PROF_ROLES + ['paciente'])
@xframe_options_sameorigin # Permite que esta vista se cargue en un iframe del mismo sitio.
def generar_hc_pdf(request, consulta_id):
    """
    Genera un PDF para una consulta de historia clínica específica.
    """
    try:
        consulta = Consulta.objects.get(id_consulta=consulta_id)
        diagnosticos = DiagnosticoPaciente.objects.filter(id_consulta=consulta)
        antecedentes = AntecedentesPaciente.objects.filter(id_paciente=consulta.id_paciente)

        # 1. Construir la URL de verificación para el QR
        verification_url = request.build_absolute_uri(
            reverse('prof_salud:ver_hc_pdf', args=[consulta.id_consulta])
        )

        # 2. Generar la imagen del QR en memoria
        qr_img = qrcode.make(verification_url, box_size=6)
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format='PNG')
        qr_b64 = base64.b64encode(qr_buffer.getvalue()).decode('utf-8')
        qr_code_data_uri = f'data:image/png;base64,{qr_b64}'

        context = {
            'consulta': consulta,
            'diagnosticos': diagnosticos,
            'antecedentes': antecedentes,
            'qr_code': qr_code_data_uri, # Pasar la imagen como Data URI
        }
        pdf = render_to_pdf('pdf/hc_pdf_template.html', context)

        if pdf:
            # Creamos la respuesta HTTP con los bytes del PDF
            response = HttpResponse(pdf, content_type='application/pdf')
            # La cabecera 'inline' sugiere al navegador mostrar el PDF en línea.
            # El navegador del usuario decide si lo muestra o lo descarga
            filename = f"hc_{consulta.id_paciente.numero_documento}_{consulta.fecha_atencion.strftime('%Y%m%d')}.pdf"
            response['Content-Disposition'] = f'inline; filename="{filename}"'
            return response
        
        messages.error(request, 'No se pudo generar el PDF.')
        return redirect('prof_salud:hc_prof_salud')

    except Consulta.DoesNotExist:
        messages.error(request, 'La consulta solicitada no existe.')
        return redirect('prof_salud:hc_prof_salud')

@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def diligenciar_omedica(request):
    profesional_id = request.session.get('id_profesional')
    if not profesional_id:
        messages.error(request, 'No se pudo identificar al profesional. Por favor, inicie sesión de nuevo.')
        return redirect('login')

    profesional = ProfesionalSalud.objects.get(id_profesional=profesional_id)

    if request.method == 'POST':
        orden_medica_form = OrdenMedicaForm(request.POST)
        servicios_formset = serviciosFormSet(request.POST, prefix='servicios')

        if orden_medica_form.is_valid() and servicios_formset.is_valid():
            try:
                # Obtenemos los datos comunes del formulario principal, pero no lo guardamos aún.
                orden_base = orden_medica_form.cleaned_data
                estado_pendiente = EstadoOrden.objects.get(nombre_estado_orden='Pendiente')
                orden_creada_id = None # Variable para guardar el ID de la última orden creada
                # Generamos un ID de lote único para esta transacción.
                lote_id = uuid.uuid4()
                fecha_emision_batch = timezone.now()

                # Guardar los servicios del formset
                for servicio_form in servicios_formset:
                    if servicio_form.cleaned_data and not servicio_form.cleaned_data.get('DELETE', False):
                        servicios_obj = servicio_form.cleaned_data.get('id_servicio')
                        # Si no hay servicio, no creamos la orden
                        if not servicios_obj:
                            continue
                    
                        # Creamos una nueva instancia de OrdenMedica para CADA servicio válido
                        nueva_orden = OrdenMedica.objects.create(
                            id_paciente=orden_base.get('id_paciente'),
                            id_tipo_orden=orden_base.get('id_tipo_orden'),
                            id_profesional=profesional,
                            id_centro_medico=profesional.id_centro_medico,
                            id_servicio=servicios_obj,
                            indicaciones=servicio_form.cleaned_data.get('indicaciones', ''),
                            id_estado_orden=estado_pendiente,
                            id_lote=lote_id, # Asignamos el ID de lote.
                            fecha_emision=fecha_emision_batch, 
                        )
                        orden_creada_id = nueva_orden.id_orden # Actualizamos el ID con la última orden

                if orden_creada_id:
                    messages.success(request, f'Orden(es) Médica(s) para el paciente {orden_base.get("id_paciente")} guardada(s) con éxito.')
                    # Redirigir a la vista PDF de la última orden creada
                    return redirect('prof_salud:ver_omedica_pdf', orden_id=orden_creada_id)
                else:
                    # Si el bucle termina y no se creó ninguna orden
                    messages.warning(request, 'No se añadió ningún servicio, por lo que no se guardó ninguna orden.')
                    return redirect('diligenciar_omedica')

            except Exception as e:
                messages.error(request, f'Ocurrió un error al guardar la orden médica: {e}')
    else:
        orden_medica_form = OrdenMedicaForm()
        servicios_formset = serviciosFormSet(prefix='servicios')

    # Preparar datos de enfermedades para JavaScript
    servicios_data = {
        e.id_servicio: {
            'codigo_servicio': e.codigo_servicio,
            'nombre_servicio': e.nombre_servicio,
            'tipo_servicio': e.tipo_servicio
        } for e in Servicios.objects.all()
    }
    servicios_json = json.dumps(servicios_data)

    return render(request, 'paginas/diligenciar_omedica.html', {
        'form': orden_medica_form, 
        'servicios_formset': servicios_formset,
        'servicios_json': servicios_json
    })

@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def ver_omedica_pdf(request, orden_id):
    """
    Muestra una página con el PDF de la Orden Médica incrustado y opciones para descargar o volver.
    """
    try:
        orden = OrdenMedica.objects.get(id_orden=orden_id)
        return render(request, 'paginas/ver_omedica_pdf.html', {'orden': orden})
    except OrdenMedica.DoesNotExist:
        messages.error(request, 'La orden médica solicitada no existe.')
        return redirect('om_prof_salud')

@role_required(allowed_roles=ALLOWED_PROF_ROLES + ['paciente'])
@xframe_options_sameorigin # Permite que esta vista se cargue en un iframe del mismo sitio.
def generar_omedica_pdf(request, orden_id):
    """
    Genera un PDF para una orden médica específica.
    """
    try:
        orden = OrdenMedica.objects.get(id_orden=orden_id)

        # Usamos el id_lote para agrupar todos los servicios de la misma orden.
        servicios_solicitados = OrdenMedica.objects.filter(
            id_lote=orden.id_lote,
            id_servicio__isnull=False
        ).select_related('id_servicio') # Optimiza la consulta para obtener los detalles del servicio

        # 1. Construir la URL de verificación para el QR
        verification_url = request.build_absolute_uri(
            reverse('prof_salud:ver_omedica_pdf', args=[orden.id_orden])
        )

        # 2. Generar la imagen del QR en memoria
        qr_img = qrcode.make(verification_url, box_size=6)
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format='PNG')
        qr_b64 = base64.b64encode(qr_buffer.getvalue()).decode('utf-8')
        qr_code_data_uri = f'data:image/png;base64,{qr_b64}'

        context = {
            'orden': orden,
            'servicios': servicios_solicitados,
            'qr_code': qr_code_data_uri,
        }
        pdf = render_to_pdf('pdf/omedica_pdf_template.html', context)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f"OM_{orden.id_paciente.numero_documento}_{orden.fecha_emision.strftime('%Y%m%d')}.pdf"
            response['Content-Disposition'] = f'inline; filename="{filename}"'
            return response
        
        messages.error(request, 'No se pudo generar el PDF de la orden médica.')
        return redirect('om_prof_salud')

    except OrdenMedica.DoesNotExist:
        messages.error(request, 'La orden médica solicitada no existe.')
        return redirect('om_prof_salud')

@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def diligenciar_omedicamentos(request):
    profesional_id = request.session.get('id_profesional')
    if not profesional_id:
        messages.error(request, 'No se pudo identificar al profesional. Por favor, inicie sesión de nuevo.')
        return redirect('login')

    profesional = ProfesionalSalud.objects.get(id_profesional=profesional_id)

    if request.method == 'POST':
        medicamento_formset = MedicamentoFormSet(request.POST, prefix='medicamentos')

        if medicamento_formset.is_valid():
            try:
                orden_creada_id = None
                lote_id = uuid.uuid4() # Generamos un ID de lote único.
                fecha_emision_batch = timezone.now()
                paciente = None # Inicializamos la variable paciente

                for form in medicamento_formset:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        nueva_orden = form.save(commit=False)
                        medicamento_seleccionado = form.cleaned_data.get('id_medicamento')
                        
                        if not medicamento_seleccionado:
                            # Si el formulario no tiene medicamento, pero ha cambiado, es un formset vacío o incompleto.
                            # Lo saltamos para no guardar una orden vacía.
                            if form.has_changed():
                                continue

                        # El paciente se toma del primer formulario válido
                        if not paciente:
                            paciente = form.cleaned_data.get('id_paciente')

                        # Asignar los datos que no vienen del formulario
                        nueva_orden.id_medicamento = medicamento_seleccionado
                        nueva_orden.id_lote = lote_id # Asignamos el ID de lote.

                        # Asignar los datos que no vienen del formulario
                        nueva_orden.id_profesional = profesional
                        nueva_orden.id_centro_medico = profesional.id_centro_medico
                        nueva_orden.fecha_emision = fecha_emision_batch
                        # Asignar un estado inicial y tipo de orden
                        nueva_orden.id_estado_orden, _ = EstadoOrden.objects.get_or_create(nombre_estado_orden__iexact='Pendiente', defaults={'nombre_estado_orden': 'Pendiente'})
                        nueva_orden.id_tipo_orden, _ = TipoOrden.objects.get_or_create(nombre_tipo__iexact='Medicamentos', defaults={'nombre_tipo': 'Medicamentos'})
                        nueva_orden.save()
                        orden_creada_id = nueva_orden.id_orden

                if orden_creada_id:
                    messages.success(request, f'Orden de Medicamentos para el paciente {nueva_orden.id_paciente} guardada con éxito.')
                    # Redirigir a la vista que muestra el PDF de la última orden creada
                    return redirect('prof_salud:ver_omedicamentos_pdf', orden_id=orden_creada_id)
                else:
                    messages.warning(request, 'No se añadió ningún medicamento, por lo que no se guardó ninguna orden.')
            except Exception as e: # Captura de otros posibles errores
                messages.error(request, f'Ocurrió un error al guardar la orden: {e}')
        else:
            # Si el formset no es válido, los errores se mostrarán en la plantilla.
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        medicamento_formset = MedicamentoFormSet(prefix='medicamentos')

    # Preparar datos de medicamentos para JavaScript
    medicamentos_data = {
        m.id_medicamento: {
            'codigo_medicamento': m.codigo_medicamento,
            'nombre_generico': m.nombre_generico,
            'principio_activo': m.principio_activo,
            'concentracion': m.concentracion,
            'forma_farmaceutica': m.forma_farmaceutica,
        } for m in Medicamentos.objects.all()
    }
    medicamentos_json = json.dumps(medicamentos_data, cls=DjangoJSONEncoder)

    return render(request, 'paginas/diligenciar_omedicamentos.html', {
        'medicamento_formset': medicamento_formset,
        'medicamentos_json': medicamentos_json,
    })

@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def ver_omedicamentos_pdf(request, orden_id):
    """
    Muestra una página con el PDF de la Orden de Medicamentos incrustado.
    """
    try:
        orden = OrdenMedica.objects.get(id_orden=orden_id)
        return render(request, 'paginas/ver_omedicamentos_pdf.html', {'orden': orden})
    except OrdenMedica.DoesNotExist:
        messages.error(request, 'La orden de medicamentos solicitada no existe.')
        return redirect('omed_prof_salud')

@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def buscar_paciente_por_documento(request):
    """
    Vista para AJAX. Busca un paciente por número de documento.
    """
    numero_documento = request.GET.get('numero_documento', None)
    if not numero_documento:
        return JsonResponse({'error': 'Número de documento no proporcionado.'}, status=400)

    try:
        paciente = Pacientes.objects.get(numero_documento=numero_documento)
        data = {
            'id_paciente': paciente.id_paciente,
            'nombre_completo': f'{paciente.nombre1} {paciente.apellido1} {paciente.apellido2}'.strip()
        }
        return JsonResponse(data)
    except Pacientes.DoesNotExist:
        return JsonResponse({'error': 'Paciente no encontrado.'}, status=404)

@role_required(allowed_roles=ALLOWED_PROF_ROLES + ['paciente'])
@xframe_options_sameorigin # Permite que esta vista se cargue en un iframe del mismo sitio.
def generar_omedicamentos_pdf(request, orden_id):
    """
    Genera un PDF para una orden de medicamentos específica.
    """
    try:
        orden = OrdenMedica.objects.get(id_orden=orden_id)

        # Usamos el id_lote para agrupar todos los medicamentos de la misma orden.
        medicamentos_solicitados = OrdenMedica.objects.filter(
            id_lote=orden.id_lote,
            id_medicamento__isnull=False # Solo órdenes que son de medicamentos
        ).select_related('id_medicamento')

        # 1. Construir la URL de verificación para el QR
        verification_url = request.build_absolute_uri(
            reverse('prof_salud:ver_omedicamentos_pdf', args=[orden.id_orden])
        )

        # 2. Generar la imagen del QR en memoria
        qr_img = qrcode.make(verification_url, box_size=6)
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format='PNG')
        qr_b64 = base64.b64encode(qr_buffer.getvalue()).decode('utf-8')
        qr_code_data_uri = f'data:image/png;base64,{qr_b64}'

        context = {
            'orden': orden,
            'medicamentos': medicamentos_solicitados,
            'qr_code': qr_code_data_uri,
        }
        pdf = render_to_pdf('pdf/omedicamentos_pdf_template.html', context)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f"OMed_{orden.id_paciente.numero_documento}_{orden.fecha_emision.strftime('%Y%m%d')}.pdf"
            response['Content-Disposition'] = f'inline; filename="{filename}"'
            return response
        
        messages.error(request, 'No se pudo generar el PDF de la orden de medicamentos.')
        return redirect('omed_prof_salud')

    except OrdenMedica.DoesNotExist:
        messages.error(request, 'La orden de medicamentos solicitada no existe.')
        return redirect('omed_prof_salud')
