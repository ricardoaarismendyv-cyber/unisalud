from django.shortcuts import render, redirect
from django.contrib import messages
from usuario.models import ProfesionalSalud, Usuarios, Roles, TipoIdentificacion, Genero, CentrosMedicos, Especialidades, DiagnosticoPaciente, AntecedentesPaciente, Enfermedades, OrdenMedica, Servicios, Consulta
from login.decorators import role_required
from .forms import ConsultaForm, DiagnosticoFormSet, AntecedenteFormSet, OrdenMedicaForm
from django.utils import timezone
import json
from django.http import HttpResponse
from django.template.loader import get_template #obtener o descargar una plantilla de diseño web
from xhtml2pdf import pisa #conversión real que realiza el trabajo de transformar el contenido HTML y CSS en el formato PDF.
from io import BytesIO #generar un archivo (como un PDF o una imagen) y enviarlo inmediatamente a un usuario a través de una API web, sin tocar el sistema de archivos del servidor.


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
            # Buscamos la última consulta atendida por este profesional
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
                paciente_obj = consulta_form.cleaned_data['paciente']
                nueva_consulta.id_paciente = paciente_obj
                nueva_consulta.save()

                # Guardar los diagnósticos del formset
                for form in diagnostico_formset:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        # El ID de la enfermedad ahora viene del campo oculto 'id_enfermedad'
                        enfermedad_obj = form.cleaned_data.get('id_enfermedad')
                        DiagnosticoPaciente.objects.create(
                            id_consulta=nueva_consulta,
                            id_enfermedad=enfermedad_obj,
                            tipo_diagnostico=form.cleaned_data['tipo_diagnostico'],
                            notas=form.cleaned_data.get('notas', ''),
                            fecha_registro=timezone.now()
                        )

                # Guardar los antecedentes del formset
                for form in antecedente_formset:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        antecedente = form.save(commit=False)
                        antecedente.id_paciente = paciente_obj
                        antecedente.fecha_registro = timezone.now().date() # Extraer solo la fecha
                        antecedente.save()

                messages.success(request, f'Historia clínica para el paciente {nueva_consulta.id_paciente} guardada con éxito.')
                return redirect('ver_hc_pdf', consulta_id=nueva_consulta.id_consulta)
            except Exception as e:
                messages.error(request, f'Ocurrió un error al guardar la historia clínica: {e}')
    else:
        consulta_form = ConsultaForm()
        diagnostico_formset = DiagnosticoFormSet(prefix='diagnosticos')
        antecedente_formset = AntecedenteFormSet(prefix='antecedentes')

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


@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def generar_hc_pdf(request, consulta_id):
    """
    Genera un PDF para una consulta de historia clínica específica.
    """
    try:
        consulta = Consulta.objects.get(id_consulta=consulta_id)
        diagnosticos = DiagnosticoPaciente.objects.filter(id_consulta=consulta)
        antecedentes = AntecedentesPaciente.objects.filter(id_paciente=consulta.id_paciente)

        context = {
            'consulta': consulta,
            'diagnosticos': diagnosticos,
            'antecedentes': antecedentes,
        }
        pdf = render_to_pdf('pdf/hc_pdf_template.html', context)

        if pdf:
            # Creamos la respuesta HTTP con los bytes del PDF
            response = HttpResponse(pdf, content_type='application/pdf')
            # Esta cabecera le indica al navegador que muestre el archivo en línea
            response['Content-Disposition'] = f'inline; filename="hc_{consulta.id_consulta}.pdf"'
            return response
        
        messages.error(request, 'No se pudo generar el PDF.')
        return redirect('hc_prof_salud')

    except Consulta.DoesNotExist:
        messages.error(request, 'La consulta solicitada no existe.')
        return redirect('hc_prof_salud')


@role_required(allowed_roles=ALLOWED_PROF_ROLES)
def diligenciar_orden_medica(request):
    """
    Vista para que el profesional de la salud diligencie una nueva orden médica.
    """
    try:
        profesional_id = request.session.get('id_profesional')
        profesional = ProfesionalSalud.objects.get(id_profesional=profesional_id)
    except ProfesionalSalud.DoesNotExist:
        messages.error(request, 'Error: Su perfil de profesional de salud no está configurado. Por favor, inicie sesión de nuevo.')
        return redirect('login')

    if request.method == 'POST':
        form = OrdenMedicaForm(request.POST)
        if form.is_valid():
            try:
                orden = form.save(commit=False)  # No guardamos en la BD todavía
                orden.id_profesional = profesional
                orden.id_centro_medico = profesional.id_centro_medico
                orden.fecha_emision = timezone.now()
                
                orden.save() # Guardamos la instancia completa en la base de datos
                
                messages.success(request, '¡Orden médica creada con éxito!')
                return redirect('om_prof_salud')  # Redirigimos a la página principal de órdenes
            except Exception as e:
                messages.error(request, f'Ocurrió un error inesperado al guardar la orden: {e}')
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = OrdenMedicaForm()

    # Obtenemos todos los servicios para pasarlos a la plantilla
    servicios = Servicios.objects.all()

    return render(request, 'paginas/diligenciar_orden_medica.html', {
        'form': form,
        'servicios': servicios,
    })
