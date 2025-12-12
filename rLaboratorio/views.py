from django.shortcuts import render, redirect
from login.decorators import role_required
from usuario.models import ProfesionalSalud, ResultadosLaboratorio
from django.urls import reverse
from django.contrib import messages
from .forms import ResultadoLaboratorioForm
from django.utils import timezone

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
        form = ResultadoLaboratorioForm(request.POST)
        if form.is_valid():
            resultado = form.save(commit=False)
            profesional_id = request.session.get('id_profesional')
            resultado.id_laboratorista = ProfesionalSalud.objects.get(id_profesional=profesional_id)
            resultado.fecha_resultado = timezone.now()
            resultado.fecha_registro = timezone.now()
            resultado.estado = 'Registrado'
            resultado.save()
            messages.success(request, f'Resultado de laboratorio para {resultado.id_paciente} guardado con éxito.')
            return redirect('rLaboratorio:inicio_laboratorista')
    else:
        form = ResultadoLaboratorioForm()

    return render(request, 'paginas/registrar_resultado.html', {'form': form})
