from django.shortcuts import render, redirect
from django.contrib.auth import logout # para manejar la sesión del usuario
from django.contrib import messages
from usuario.models import Usuarios, pacientes, profesionalsalud

def login_view(request):
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre_usuario')
        contrasena = request.POST.get('contrasena')
        try:
            usuario = Usuarios.objects.get(nombre_usuario=nombre_usuario)
            if usuario.check_password(contrasena):
                request.session['id_usuario'] = usuario.id_usuario
                request.session['nombre_rol'] = usuario.id_rol.nombre_rol # Corregido: La relación es a través de id_rol

                if usuario.id_rol.nombre_rol == 'paciente': # Corregido: La relación es a través de id_rol
                    try:
                        paciente = pacientes.objects.get(usuario=usuario)
                        request.session['id_paciente'] = paciente.id_paciente
                        return redirect('inicio-usuario')
                    except pacientes.DoesNotExist:
                        messages.error(request, 'Este usuario no tiene un perfil de paciente asociado.')
                        return render(request, 'paginas/login.html')
                
                elif usuario.id_rol.nombre_rol in ['profesional_salud', 'laboratorista', 'recepcionista', 'admin_centro_medico']: # Corregido: La relación es a través de id_rol
                    try:
                        prof_salud = profesionalsalud.objects.get(usuario=usuario)
                        request.session['id_profesional'] = prof_salud.id_profesional
                        return redirect('inicio_prof_salud')
                    except profesionalsalud.DoesNotExist:
                        messages.error(request, 'Este usuario no tiene un perfil de profesional de salud asociado.')
                        return render(request, 'paginas/login.html')
                else:
                    messages.error(request, 'Rol no reconocido o sin página de inicio definida.')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
        except Usuarios.DoesNotExist:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    return render(request, 'paginas/login.html')

# para cerrar sesion y redirige al login
def logout_view(request):
    logout(request)
    return redirect('login')