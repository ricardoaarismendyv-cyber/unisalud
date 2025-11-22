from django.shortcuts import render, redirect
from login.decorators import role_required
from .models import pacientes, Usuarios, Roles, tipoidentificacion, genero
from django.contrib import messages

@role_required(allowed_roles=['paciente'])
def inicio_usuario(request):
    try:
        # Obtener el ID del paciente desde la sesión
        paciente_id = request.session.get('id_paciente')
        paciente = pacientes.objects.get(id_paciente=paciente_id)
        return render(request, 'paginas/inicio-usuario.html', {'paciente': paciente})
    except pacientes.DoesNotExist:
        messages.error(request, 'No se encontró el perfil del paciente.')
        return redirect('login')

@role_required(allowed_roles=['paciente'])
def hcusuario(request):
    return render(request, 'paginas/historia-clinica-usuario.html')

@role_required(allowed_roles=['paciente'])
def omusuario(request):
    return render(request, 'paginas/orden-medica-usuario.html')

@role_required(allowed_roles=['paciente'])
def omeusuario(request):
    return render(request, 'paginas/orden-medicamentos-usuario.html')

@role_required(allowed_roles=['paciente'])
def turnosusuario(request):
    return render(request, 'paginas/turnos-usuario.html')

# Las siguientes vistas pueden ser públicas, no requieren login
def preguntasfrecuentes(request):
    return render(request, 'paginas/preguntas-frecuentes.html')

def usosistema(request):
    return render(request, 'paginas/uso-sistema.html')

def buzonsugerencias(request):
    return render(request, 'paginas/buzon-sugerencias.html')

# Registror nuevos usuarios-pacientes
def registro(request):
    # Cargar datos para los <select> del formulario
    tipos_id = tipoidentificacion.objects.all()
    generos = genero.objects.all()
    context = {
        'tipos_identificacion': tipos_id,
        'generos': generos
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
            #Asigna al nuevo usuario el rol paciente
            nuevo_usuario = Usuarios(
                nombre_usuario=nombre_usuario,
                email=email,
                id_rol=rol_paciente, #se asigna el rol paciente
            )
            nuevo_usuario.set_password(contrasena) # Hashear (huella digital, identificador unico, asegura la integridad de los datos) y guardar contraseña
            nuevo_usuario.save()

            # Para crear el Perfil del Paciente 
            # Se obtienen de las llaves foráneas.
            tipo_id_obj = tipoidentificacion.objects.get(id_tipo_identificacion=request.POST.get('tipoDocumento'))
            genero_obj = genero.objects.get(id_genero=request.POST.get('genero'))

            pacientes.objects.create(
                usuario=nuevo_usuario,
                nombre1=request.POST.get('primerNombre'),
                nombre2=request.POST.get('segundoNombre'),
                apellido1=request.POST.get('primerApellido'),
                apellido2=request.POST.get('segundoApellido'),
                numero_documento=request.POST.get('numeroDocumento'),
                id_tipo_identificacion=tipo_id_obj,
                fecha_nacimiento=request.POST.get('fechaNacimiento'),
                id_genero=genero_obj,
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

def contactanos(request):
    return render(request, 'paginas/contactanos.html')
