from django.shortcuts import render, redirect
from django.contrib.auth import logout # para manejar la sesión del usuario
from django.contrib import messages
from usuario.models import Usuarios, Pacientes, ProfesionalSalud

def login_view(request):
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre_usuario')
        contrasena = request.POST.get('contrasena')
        try:
            usuario = Usuarios.objects.get(nombre_usuario=nombre_usuario)
            if usuario.check_password(contrasena):
                request.session['id_usuario'] = usuario.id_usuario
                
                # Obtenemos una lista de los nombres de los roles del usuario
                roles_usuario = [rol.nombre_rol for rol in usuario.roles.all()]
                request.session['roles'] = roles_usuario

                # Intentamos cargar el perfil de paciente si el rol existe
                if 'paciente' in roles_usuario:
                    try:
                        paciente = Pacientes.objects.get(usuario=usuario)
                        request.session['id_paciente'] = paciente.id_paciente
                    except Pacientes.DoesNotExist:
                        messages.warning(request, 'El usuario tiene el rol de paciente, pero no un perfil de paciente asociado.')

                # Intentamos cargar el perfil profesional si el rol existe
                roles_profesionales = ['profesional_salud', 'laboratorista', 'recepcionista', 'admin_centro_medico']
                if any(rol in roles_profesionales for rol in roles_usuario):
                    try:
                        prof_salud = ProfesionalSalud.objects.get(usuario=usuario)
                        request.session['id_profesional'] = prof_salud.id_profesional
                    except ProfesionalSalud.DoesNotExist:
                        messages.warning(request, 'El usuario tiene un rol profesional, pero no un perfil de profesional de salud asociado.')

                # Priorizamos roles de personal de salud
                if any(rol in roles_profesionales for rol in roles_usuario):
                    if 'id_profesional' in request.session:
                        return redirect('profesionalS/turnos/')
                # Si no es profesional, verificamos si es paciente
                elif 'paciente' in roles_usuario:
                    if 'id_paciente' in request.session:
                        return redirect('inicio-usuario')
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