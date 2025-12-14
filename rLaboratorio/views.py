from django.shortcuts import render, redirect
from login.decorators import role_required
from usuario.models import ProfesionalSalud, ResultadosLaboratorio
from prof_salud.views import ALLOWED_PROF_ROLES # Importamos los roles de prof_salud
from django.urls import reverse
from django.contrib import messages
from .forms import ResultadoLaboratorioForm
from django.utils import timezone

from django.http import HttpResponse, Http404

# Roles permitidos para esta seccion
ALLOWED_LAB_ROLES = ['laboratorista', 'admin_centro_medico']

@role_required(allowed_roles=ALLOWED_LAB_ROLES)
def inicio_laboratorista(request):
    try:
        profesional_id = request.session.get('id_profesional')
        if not profesional_id:
            messages.error(request, 'No se encontró un perfil de profesional en su sesión.')
            return redirect('login')

        # Aseguramos que el rol activo sea 'laboratorista' si el usuario tiene múltiples roles
        request.session['active_role'] = 'laboratorista'
        profesional = ProfesionalSalud.objects.get(id_profesional=profesional_id)
        
        # Obtenemos los últimos 5 resultados registrados por este laboratorista
        ultimos_resultados = ResultadosLaboratorio.objects.filter(id_laboratorista=profesional).order_by('-fecha_registro')[:5]

        return render(request, 'paginas/inicio_laboratorista.html', {
            'profesional': profesional,
            'roles': request.session.get('roles', []),
            'ultimos_resultados': ultimos_resultados
        })
    except ProfesionalSalud.DoesNotExist:
        messages.error(request, 'No se encontró el perfil del profesional de salud.')
        return redirect('login')

@role_required(allowed_roles=ALLOWED_LAB_ROLES)
def registrar_resultado(request):
    profesional_id = request.session.get('id_profesional')
    if not profesional_id:
        messages.error(request, 'No se pudo identificar al profesional. Por favor, inicie sesión de nuevo.')
        return redirect('login')

    profesional = ProfesionalSalud.objects.get(id_profesional=profesional_id)

    if request.method == 'POST':
        form = ResultadoLaboratorioForm(request.POST, request.FILES)
        if form.is_valid():
            resultado = form.save(commit=False)
            resultado.id_laboratorista = profesional
            resultado.fecha_resultado = timezone.now()
            resultado.fecha_registro = timezone.now()
            resultado.estado = 'Registrado'
            resultado.save()
            messages.success(request, f'Resultado de laboratorio para {resultado.id_paciente} guardado con éxito.')
            # Redirigir a la nueva vista para mostrar el PDF
            return redirect('rLaboratorio:ver_resultado_pdf', resultado_id=resultado.id_resultado)
    else:
        form = ResultadoLaboratorioForm()

    return render(request, 'paginas/registrar_resultado.html', {'form': form})

@role_required(allowed_roles=ALLOWED_LAB_ROLES)
def ver_resultado_pdf(request, resultado_id):
    """
    Muestra una página con el PDF del resultado de laboratorio incrustado.
    """
    try:
        resultado = ResultadosLaboratorio.objects.get(id_resultado=resultado_id)
        return render(request, 'paginas/ver_resultado_pdf.html', {'resultado': resultado})
    except ResultadosLaboratorio.DoesNotExist:
        messages.error(request, 'El resultado de laboratorio solicitado no existe.')
        return redirect('rLaboratorio:inicio_laboratorista')

@role_required(allowed_roles=ALLOWED_LAB_ROLES + ALLOWED_PROF_ROLES)
def generar_resultado_pdf_vista(request, resultado_id):
    """
    Sirve el archivo PDF para ser mostrado en un <iframe/> o <object/>.
    """
    try:
        resultado = ResultadosLaboratorio.objects.get(id_resultado=resultado_id)
        if resultado.archivo_pdf:
            return HttpResponse(resultado.archivo_pdf.read(), content_type='application/pdf')
        else:
            raise Http404("No se encontró el archivo PDF para este resultado.")
    except (ResultadosLaboratorio.DoesNotExist, FileNotFoundError):
        raise Http404("El resultado o el archivo no existe.")
