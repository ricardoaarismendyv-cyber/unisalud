from django.shortcuts import render, redirect
from django.contrib import messages
from usuario.models import ProfesionalSalud, Usuarios, Roles, TipoIdentificacion, Genero, CentrosMedicos, Especialidades, DiagnosticoPaciente, AntecedentesPaciente, Enfermedades
from login.decorators import role_required
from .forms import ConsultaForm, DiagnosticoFormSet, AntecedenteFormSet
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
                        DiagnosticoPaciente.objects.create(
                            id_consulta=nueva_consulta,
                            id_enfermedad=form.cleaned_data['id_enfermedad'],
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
                return redirect('generar_hc_pdf', consulta_id=nueva_consulta.id_consulta)
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
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


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
        return HttpResponse(pdf, content_type='application/pdf')

    except Consulta.DoesNotExist:
        messages.error(request, 'La consulta solicitada no existe.')
        return redirect('hc_prof_salud')
