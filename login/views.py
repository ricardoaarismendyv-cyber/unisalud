from django.shortcuts import render, redirect
from django.contrib.auth import logout # para manejar la sesión del usuario
from django.contrib import messages
from usuario.models import Usuarios, Pacientes, ProfesionalSalud, Roles, TipoIdentificacion, Genero, EstadoCivil, GrupoRh, EstratoSocioeconomico

def login_view(request):
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre_usuario')
        contrasena = request.POST.get('contrasena')

        try:
            usuario = Usuarios.objects.get(nombre_usuario=nombre_usuario)

            if usuario.check_password(contrasena):

                # Guardar id_usuario
                request.session['id_usuario'] = usuario.id_usuario

                # Guardar roles
                roles_usuario = [rol.nombre_rol for rol in usuario.roles.all()]
                request.session['roles'] = roles_usuario

                # ----------------------
                # PERFIL PACIENTE
                # ----------------------
                if 'paciente' in roles_usuario:
                    try:
                        paciente = Pacientes.objects.get(usuario=usuario)
                        request.session['id_paciente'] = paciente.id_paciente
                    except Pacientes.DoesNotExist:
                        messages.warning(request, 'El usuario tiene el rol de paciente, pero no un perfil asociado.')

                # ----------------------
                # PERFIL PROFESIONAL
                # ----------------------
                roles_prof = ['profesional_salud', 'laboratorista', 'recepcionista', 'admin_centro_medico']

                if any(r in roles_prof for r in roles_usuario):
                    try:
                        profesional = ProfesionalSalud.objects.get(usuario=usuario)
                        request.session['id_profesional'] = profesional.id_profesional
                    except ProfesionalSalud.DoesNotExist:
                        messages.warning(request, 'El usuario es profesional, pero no tiene perfil asignado.')

                # ----------------------
                # REDIRECCIÓN PRINCIPAL
                # ----------------------

                # Si es profesional → IR DIRECTO A TURNOS
                if any(r in roles_prof for r in roles_usuario):
                    return redirect(
                        'consultas_prof_salud',
                        id_prof=request.session['id_profesional']
                    )

                # Si es paciente
                if 'paciente' in roles_usuario:
                    return redirect('inicio-usuario')

                messages.error(request, 'Rol no reconocido.')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')

        except Usuarios.DoesNotExist:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')

    return render(request, 'paginas/login.html')

# para cerrar sesion y redirige al login
def logout_view(request):
    logout(request)
    return redirect('login')


# Registror nuevos usuarios-pacientes
def registro(request):
    # Cargar datos para los <select> del formulario
    tipos_id = TipoIdentificacion.objects.all()
    generos = Genero.objects.all()
    estados_civiles = EstadoCivil.objects.all()
    grupos_rh = GrupoRh.objects.all()
    estratos = EstratoSocioeconomico.objects.all()
    context = {
        'tipos_identificacion': tipos_id,
        'generos': generos,
        'estados_civiles': estados_civiles,
        'grupos_rh': grupos_rh,
        'estratos': estratos
    }
    if request.method == 'POST':
        # Obtener los datos cuando se diligencia el formulario
        nombre_usuario = request.POST.get('nombre_usuario')
        email = request.POST.get('email')
        contrasena = request.POST.get('password')
        confirm_contrasena = request.POST.get('confirmPassword')

        # permite añadir nuevamente los valores del POST llenar el formulario en caso de error
        context['form_values'] = request.POST

        # Validaciones básicas de usuario
        if contrasena != confirm_contrasena:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'paginas/registro.html', context)

        if Usuarios.objects.filter(nombre_usuario=nombre_usuario).exists():
            messages.error(request, f'El nombre de usuario "{nombre_usuario}" ya está en uso.')
            return render(request, 'paginas/registro.html', context)

        if Usuarios.objects.filter(email=email).exists():
            messages.error(request, f'El correo electrónico "{email}" ya está registrado.')
            return render(request, 'paginas/registro.html', context)

        # Se crea el Usuario con rol paciente
        try:
            #busca el rol paciente
            rol_paciente = Roles.objects.get(nombre_rol='paciente')
            #Crea el nuevo usuario
            nuevo_usuario = Usuarios(
                nombre_usuario=nombre_usuario,
                email=email,
            )
            nuevo_usuario.set_password(contrasena) # Hashear (huella digital, identificador unico, asegura la integridad de los datos) y guardar contraseña
            nuevo_usuario.save()
            nuevo_usuario.roles.add(rol_paciente) # Asigna el rol paciente usando la relación ManyToMany

            # Para crear el Perfil del Paciente 
            # Se obtienen de las llaves foráneas.
            tipo_id_obj = TipoIdentificacion.objects.get(id_tipo_identificacion=request.POST.get('tipoDocumento'))
            genero_obj = Genero.objects.get(id_genero=request.POST.get('genero'))
            estado_civil_obj = EstadoCivil.objects.get(id_estado_civil=request.POST.get('estadoCivil')) if request.POST.get('estadoCivil') else None
            grupo_rh_obj = GrupoRh.objects.get(id_rh=request.POST.get('grupoRh')) if request.POST.get('grupoRh') else None
            estrato_obj = EstratoSocioeconomico.objects.get(id_estrato=request.POST.get('estrato')) if request.POST.get('estrato') else None

            Pacientes.objects.create(
                usuario=nuevo_usuario,
                nombre1=request.POST.get('primerNombre'),
                nombre2=request.POST.get('segundoNombre'),
                apellido1=request.POST.get('primerApellido'),
                apellido2=request.POST.get('segundoApellido'),
                numero_documento=request.POST.get('numeroDocumento'),
                id_tipo_identificacion=tipo_id_obj,
                fecha_nacimiento=request.POST.get('fechaNacimiento'),
                id_genero=genero_obj,
                id_estado_civil=estado_civil_obj,
                id_rh=grupo_rh_obj,
                id_estrato=estrato_obj,
                direccion=request.POST.get('direccion'),
                telefono=request.POST.get('telefono'),    
                celular=request.POST.get('celular'),
                correo_electronico=email 
            )

            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('login')

        except Roles.DoesNotExist:
            messages.error(request, 'El rol "paciente" no está configurado en el sistema. Contacta al administrador.')
            return render(request, 'paginas/registro.html', context)
        except Exception as e:
            messages.error(request, f'Ocurrió un error inesperado: {e}')
            # Opcional: se puede eliminar el usuario si la creación del paciente falla
            if 'nuevo_usuario' in locals() and nuevo_usuario.pk:
                nuevo_usuario.delete()
            return render(request, 'paginas/registro.html', context)

    # Para una petición GET, simplemente renderiza el formulario con el contexto
    return render(request, 'paginas/registro.html', context)
