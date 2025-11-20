from django.shortcuts import render, redirect
from django.contrib import messages
from usuario.models import profesionalsalud


def inicio_prof_salud(request):
        # Verificar si el usuario es un profesional de la salud
        if request.session.get('nombre_rol') not in ['profesional_salud', 'laboratorista', 'recepcionista', 'admin_centro_medico']:
                messages.error(request, 'Acceso no autorizado.')
                return redirect('login')

        try:
                # Obtener el ID del profesional desde la sesión y buscar el objeto
                profesional_id = request.session.get('id_profesional')
                profesional = profesionalsalud.objects.get(id_profesional=profesional_id)
                return render(request, 'paginas/inicio_prof_salud.html', {'profesional': profesional})
        except profesionalsalud.DoesNotExist:
                messages.error(request, 'No se encontró el perfil del profesional de salud.')
                return redirect('login')

def hc_prof_salud(request):
    return render(request, 'paginas/hc_prof_salud.html') #Vista de Historia Clínica para el profesional de salud

def om_prof_salud(request):
    return render(request, 'paginas/om_prof_salud.html') #Vista de Orden Médica para el profesional de salud

def omed_prof_salud(request):
    return render(request, 'paginas/omed_prof_salud.html') #Vista de Orden de Medicamentos para el profesional de salud.

def consultas_prof_salud(request):
    return render(request, 'paginas/consultas_prof_salud.html') #Vista de Turnos/Agendamiento para el profesional de salud

def registro_prof_salud(request):
    return render(request, 'paginas/registro_prof_salud.html') #Vista para el formulario de registro de nuevos usuarios.   

def preguntasfrecuentes_prof_salud(request):
    return render(request, 'paginas/preguntas-frecuentes_prof_salud.html')

def usosistema_prof_salud(request):
    return render(request, 'paginas/uso-sistema_prof_salud.html')

def buzonsugerencias_prof_salud(request):
    return render(request, 'paginas/buzon-sugerencias_prof_salud.html')

def contactanos_prof_salud(request):
    return render(request, 'paginas/contactanos_prof_salud.html')
