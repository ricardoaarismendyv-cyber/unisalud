from django.shortcuts import render, redirect
from django.contrib import messages
from usuario.models import Usuarios, Pacientes, ProfesionalSalud

def login_view(request):
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre_usuario')
        contrasena = request.POST.get('contrasena')
        
        try:
            usuario = Usuarios.objects.get(nombre_usuario=nombre_usuario)
            
            if usuario.check_password(contrasena):
                # 1. Guardar datos básicos en sesión
                request.session['id_usuario'] = usuario.id_usuario
                request.session['nombre_usuario'] = usuario.nombre_usuario
                request.session['email'] = usuario.email
                request.session['roles'] = list(usuario.roles.values_list('nombre_rol', flat=True))
                
                print(f"✅ Usuario logueado: {usuario.nombre_usuario}")
                print(f"📋 Roles: {request.session['roles']}")
                
                # 2. Si es PACIENTE
                if 'paciente' in request.session['roles']:
                    try:
                        paciente = Pacientes.objects.get(usuario=usuario)
                        request.session['id_paciente'] = paciente.id_paciente
                        print(f"✅ ID Paciente guardado: {paciente.id_paciente}")
                        messages.success(request, f'Bienvenido {usuario.nombre_usuario}')
                        return redirect('inicio-usuario')
                    except Pacientes.DoesNotExist:
                        messages.error(request, f'Tu cuenta de usuario existe, pero no tienes un perfil de paciente creado. Contacta al administrador.')
                        print(f"❌ Usuario {usuario.nombre_usuario} no tiene registro en tabla pacientes")
                        return redirect('login')
                
                # 3. Si es PROFESIONAL
                if any(rol in request.session['roles'] for rol in ['profesional_salud', 'laboratorista', 'recepcionista', 'admin_centro_medico']):
                    print(f"🔍 Buscando perfil profesional para usuario ID: {usuario.id_usuario}")
                    try:
                        profesional = ProfesionalSalud.objects.get(usuario=usuario)
                        request.session['id_profesional'] = profesional.id_profesional
                        print(f"✅ ID Profesional guardado: {profesional.id_profesional}")
                        messages.success(request, f'Bienvenido {usuario.nombre_usuario}')
                        
                        # Redirigir según rol
                        if 'profesional_salud' in request.session['roles']:
                            return redirect('inicio_prof_salud')
                        elif 'admin_centro_medico' in request.session['roles']:
                            return redirect('inicio_admin')
                        else:
                            return redirect('inicio_prof_salud')
                        
                    except ProfesionalSalud.DoesNotExist:
                        messages.error(request, f'Tu cuenta existe pero no tienes un perfil profesional. Contacta al administrador del sistema.')
                        print(f"❌ Usuario {usuario.nombre_usuario} tiene roles {request.session['roles']} pero no existe en profesionalsalud")
                        print(f"   Verifica que exista un registro en la tabla profesionalsalud con usuario_id={usuario.id_usuario}")
                        return redirect('login')
                
                # Si llegó aquí, tiene un rol que no está manejado
                messages.error(request, f'Tu rol ({", ".join(request.session["roles"])}) no está configurado correctamente.')
                return redirect('login')
            else:
                messages.error(request, 'Contraseña incorrecta.')
        
        except Usuarios.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'paginas/login.html')

def logout_view(request):
    # Limpiar toda la sesión
    request.session.flush()
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')