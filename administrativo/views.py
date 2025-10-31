from django.shortcuts import render, redirect

# Create your views here.

def inicio_unisalud(request):
    if request.user.is_authenticated:
        if request.user.is_paciente:
            return redirect('inicio_paciente')
        elif request.user.is_profesional:
            return redirect('inicio_profesionalS')
        elif request.user.is_admin:
            return redirect('inicio_admin')
    return render(request, 'paginas/inicio_unisalud.html')

def login_admin(request):
    return render(request, 'paginas/login_admin.html')

def inicio_admin(request):
    return render(request, 'paginas/inicio_admin.html')

def registro_admin(request):
    return render(request, 'paginas/registro_admin.html')

def hc_admin(request):
    return render(request, 'paginas/hc_admin.html')

def buzonsugerencias_admin(request):
    return render(request, 'paginas/buzon-sugerencias_admin.html')

def gestion_admin(request):
    return render(request, 'paginas/gestion_admin.html')

def hc_admin(request):
    return render(request, 'paginas/hc_admin.html')

def om_admin(request):
    return render(request, 'paginas/om_admin.html')

def omed_admin(request):
    return render(request, 'paginas/omed_admin.html')

def preguntasfrecuentes_admin(request):
    return render(request, 'paginas/preguntas-frecuentes_admin.html')

def usosistema_admin(request):
    return render(request, 'paginas/uso-sistema_admin.html')

def contactanos_admin(request):
    return render(request, 'paginas/contactanos_admin.html')

def turnos_admin(request):
    return render(request, 'paginas/turnos_admin.html')