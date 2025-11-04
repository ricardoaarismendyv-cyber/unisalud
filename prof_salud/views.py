from django.shortcuts import render, redirect

# Create your views here.

def inicio_prof_salud(request):
    return render(request, 'paginas/inicio_prof_salud.html') #Vista de inicio para el profesional de salud

def login_prof_salud(request):
    return render(request, 'paginas/login_prof_salud.html' ) #Vista para el formulario de inicio de sesión

def logout_prof_salud(request):
    logout(request)
    return redirect('inicio_prof_salud') #Redirige a la página de inicio general tras cerrar sesión.

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

