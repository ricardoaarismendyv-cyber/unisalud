from django.shortcuts import render, redirect
from login.decorators import role_required
from django.contrib import messages
from django.http import JsonResponse
from usuario.models import TipoIdentificacion, Genero, Pacientes, Usuarios, Roles, ProfesionalSalud, CentrosMedicos, Especialidades, EstadoCivil, GrupoRh, EstratoSocioeconomico, Eps, TiposAfiliacion, Afiliacion, Medicamentos  # Importar modelos necesarios
from django.contrib.auth.hashers import make_password # Para encriptar la contraseña
from datetime import datetime

# Create your views here.
ALLOWED_ADMIN_ROLES = ['admin_centro_medico']

def login_admin(request):
    return render(request, 'paginas/login_admin.html')

@role_required(allowed_roles=ALLOWED_ADMIN_ROLES)
def inicio_admin(request):
    return render(request, 'paginas/inicio_admin.html')

@role_required(allowed_roles=ALLOWED_ADMIN_ROLES)
def gestion_admin(request):
    # 1. Consultar la base de datos para obtener los datos necesarios
    tipos_id = TipoIdentificacion.objects.all()
    generos = Genero.objects.all()
    centros_medicos = CentrosMedicos.objects.all()
    especialidades = Especialidades.objects.all()
    estados_civiles = EstadoCivil.objects.all()
    grupos_rh = GrupoRh.objects.all()
    estratos = EstratoSocioeconomico.objects.all()
    pacientes = Pacientes.objects.all()
    epss = Eps.objects.all()
    tipos_afiliacion = TiposAfiliacion.objects.all()
    medicamentos = Medicamentos.objects.all()
    # 2. Crear un diccionario de contexto para pasar los datos a la plantilla
    context = {
        'tipos_identificacion': tipos_id, 'generos': generos, 'centros_medicos': centros_medicos, 
        'especialidades': especialidades, 'estados_civiles': estados_civiles, 'grupos_rh': grupos_rh, 
        'estratos': estratos, 'pacientes': pacientes, 'epss': epss, 'tipos_afiliacion': tipos_afiliacion,
        'medicamentos': medicamentos
    }
    # 3. Renderizar la plantilla pasándole el contexto
    return render(request, 'paginas/gestion_admin.html', context)

def hc_admin(request):
    return render(request, 'paginas/hc_admin.html')

def buzonsugerencias_admin(request):
    return render(request, 'paginas/buzon-sugerencias_admin.html')

def agregar_usuario(request):
    if request.method == 'POST':
        # Lógica para procesar el formulario de registro de usuario
        # No es necesario el if 'primerNombre' in request.POST aquí, ya que esta vista es específica para agregar_usuario
            primer_nombre = request.POST.get('primerNombre')
            segundo_nombre = request.POST.get('segundoNombre', '')
            primer_apellido = request.POST.get('primerApellido')
            segundo_apellido = request.POST.get('segundoApellido', '')
            numero_documento = request.POST.get('numeroDocumento')
            tipo_documento_id = request.POST.get('tipoDocumento')
            fecha_nacimiento = request.POST.get('fechaNacimiento')
            genero_id = request.POST.get('genero')
            estrato=request.POST.get('estrato')
            grupo_rh=request.POST.get('rh')
            estado_civil=request.POST.get('estadoCivil')
            direccion = request.POST.get('direccion') or None # Si el campo viene vacío o no existe, se asigna None
            telefono = request.POST.get('telefono') or None   # Si el campo viene vacío o no existe, se asigna None
            celular = request.POST.get('celular')
            nombre_usuario = request.POST.get('nombre_usuario')
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            # --- INICIO DE LA CORRECCIÓN ---
            try:
                # 1. Crear el usuario de Django (Usuarios)
                nuevo_usuario_django = Usuarios(
                    nombre_usuario=nombre_usuario,
                    email=email,
                    numero_documento=numero_documento, # <-- AÑADIDO: Guardar documento en Usuarios
                )
                nuevo_usuario_django.set_password(password) # Usar el método para encriptar
                nuevo_usuario_django.save()

                # 2. Asignar el rol de paciente
                rol_paciente = Roles.objects.get(nombre_rol='paciente')
                nuevo_usuario_django.roles.add(rol_paciente)

                # 3. Obtener objetos foráneos para el Paciente
                tipo_id = TipoIdentificacion.objects.get(id_tipo_identificacion=tipo_documento_id)
                genero_id = Genero.objects.get(id_genero=genero_id)

                # 4. Crear el perfil del paciente (Pacientes) asociado al usuario
                Pacientes.objects.create(
                    usuario=nuevo_usuario_django,
                    id_tipo_identificacion=tipo_id,
                    numero_documento=numero_documento,
                    nombre1=primer_nombre,
                    nombre2=segundo_nombre,
                    apellido1=primer_apellido,
                    apellido2=segundo_apellido,
                    id_genero=genero_id,
                    id_estrato=estrato,
                    id_rh=grupo_rh,
                    id_estado_civil=estado_civil,
                    fecha_nacimiento=fecha_nacimiento,
                    direccion=direccion,
                    celular=celular,
                    telefono=telefono,
                    correo_electronico=email
                )
                messages.success(request, '¡Usuario y perfil de paciente creados con éxito!')
            except Exception as e:
                messages.error(request, f'Ocurrió un error al registrar el usuario: {e}')
            
            return redirect('gestion_admin')
            # --- FIN DE LA CORRECCIÓN ---
    # Si es una petición GET a esta URL, redirigimos a la página principal de gestión
    return redirect('gestion_admin')

def eliminar_profesional(request):
    if request.method == 'POST':
        # ¿Es el formulario de eliminar profesional?
        if 'documento_profesional' in request.POST:
            documento = request.POST.get('documento_profesional')
            try:
                # Buscamos al profesional por su número de documento
                profesional_a_eliminar = ProfesionalSalud.objects.get(numero_documento=documento)
                
                # Si lo encontramos, eliminamos el usuario asociado y el perfil del profesional
                # El OneToOneField con on_delete=models.CASCADE se encarga de esto si el usuario se elimina.
                nombre_completo = f'{profesional_a_eliminar.nombre1} {profesional_a_eliminar.apellido1}' # Guardamos el nombre antes de borrar
                profesional_a_eliminar.delete()
                
                messages.success(request, f'El profesional {nombre_completo} ha sido eliminado con éxito.')

            except ProfesionalSalud.DoesNotExist:
                messages.error(request, f'No se encontró ningún profesional con el documento número {documento}.')
            except ProfesionalSalud.MultipleObjectsReturned:
                messages.error(request, f'Error: Se encontraron múltiples profesionales con el documento {documento}. Contacte al soporte técnico.')
            except Exception as e:
                messages.error(request, f'Ocurrió un error inesperado: {e}')
            
            return redirect('gestion_admin')

        # Aquí puedes añadir 'elif' para los otros formularios (modificar, agregar profesional, etc.)

    # Si la petición es GET, simplemente mostramos la página con los datos para los desplegables
    tipos_id = TipoIdentificacion.objects.all()
    generos = Genero.objects.all()
    context = {'tipos_identificacion': tipos_id, 'generos': generos}
    return render(request, 'paginas/gestion_admin.html', context)


@role_required(allowed_roles=ALLOWED_ADMIN_ROLES)
def buscar_usuario_por_documento(request):
    documento = request.GET.get('numero_documento')
    if not documento:
        return JsonResponse({'status': 'error', 'message': 'Debe proporcionar un número de documento.'}, status=400)

    # 1. Verificar si ya existe como ProfesionalSalud
    if ProfesionalSalud.objects.filter(numero_documento=documento).exists():
        return JsonResponse({
            'status': 'error',
            'message': 'Este usuario ya tiene un rol como profesional de la salud.'
        }, status=409) # 409 Conflict

    # 2. Buscar si existe como Usuario y si tiene perfil de Paciente
    try:
        # Buscamos primero en la tabla Usuarios
        usuario = Usuarios.objects.get(numero_documento=documento)
        
        # Verificamos si tiene un perfil de paciente para autocompletar
        try:
            paciente = Pacientes.objects.select_related('id_tipo_identificacion', 'id_genero').get(usuario=usuario)
            datos_paciente = {
                'id_usuario': usuario.id_usuario,
                'nombre1': paciente.nombre1,
                'nombre2': paciente.nombre2 or '',
                'apellido1': paciente.apellido1,
                'apellido2': paciente.apellido2 or '',
                'id_tipo_identificacion': paciente.id_tipo_identificacion.id_tipo_identificacion,
                'numero_documento': paciente.numero_documento,
                'id_genero': paciente.id_genero.id_genero,
                'celular': paciente.celular or '',
                'email': usuario.email,
            }
            return JsonResponse({'status': 'paciente_encontrado', 'data': datos_paciente})
        except Pacientes.DoesNotExist:
            # Si el usuario existe pero no es paciente (caso raro), lo tratamos como no encontrado para crear perfil
            return JsonResponse({'status': 'no_encontrado', 'message': 'Usuario sin perfil de paciente. Puede crear uno nuevo.'})

    except Usuarios.DoesNotExist:
        # 3. Si no existe como paciente ni profesional, es un usuario nuevo
        return JsonResponse({'status': 'no_encontrado', 'message': 'No se encontró usuario. Puede crear uno nuevo.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def agregar_profesional(request):
    if request.method == 'POST':
        try:
            id_usuario_existente = request.POST.get('id_usuario_existente')
            # --- Datos del Usuario ---
            nombre_usuario = request.POST.get('nombre_usuario_prof')
            email = request.POST.get('email_prof')
            password = request.POST.get('password_prof')
            rol_nombre = request.POST.get('rol_prof') # 'profesional_salud', 'recepcionista', etc.

            # --- Datos del Perfil Profesional ---
            primer_nombre = request.POST.get('primerNombre_prof')
            segundo_nombre = request.POST.get('segundoNombre_prof', '')
            primer_apellido = request.POST.get('primerApellido_prof')
            segundo_apellido = request.POST.get('segundoApellido_prof', '')
            tipo_documento_id = request.POST.get('tipoDocumento_prof')
            numero_documento = request.POST.get('numeroDocumento_prof')
            genero_id = request.POST.get('genero_prof')
            celular = request.POST.get('celular_prof')
            registro_profesional = request.POST.get('registro_profesional', '')
            especialidad_id = request.POST.get('especialidad_prof')
            centro_medico_id = request.POST.get('centro_medico_prof')

            if ProfesionalSalud.objects.filter(numero_documento=numero_documento, id_tipo_identificacion=tipo_documento_id).exists():
                messages.error(request, f'Ya existe un profesional registrado con el documento {numero_documento}.')
                return redirect('gestion_admin')

            if id_usuario_existente:
                # --- LÓGICA PARA ACTUALIZAR PACIENTE A PROFESIONAL ---
                usuario_a_actualizar = Usuarios.objects.get(id_usuario=id_usuario_existente)
                # No se cambian usuario, email ni contraseña. Solo se añade el rol.
                
            else:
                # --- LÓGICA PARA CREAR NUEVO USUARIO Y PROFESIONAL ---
                # Validaciones para nuevo usuario
                if Usuarios.objects.filter(nombre_usuario=nombre_usuario).exists():
                    messages.error(request, f'El nombre de usuario "{nombre_usuario}" ya está en uso.')
                    return redirect('gestion_admin')
                
                if Usuarios.objects.filter(email=email).exists():
                    messages.error(request, f'El correo electrónico "{email}" ya está registrado.')
                    return redirect('gestion_admin')

                # 1. Crear el usuario de Django (Usuarios)
                nuevo_usuario = Usuarios(
                    nombre_usuario=nombre_usuario,
                    email=email,
                    numero_documento=numero_documento, # <-- AÑADIDO: Guardar documento en Usuarios
                )
                nuevo_usuario.set_password(password)
                nuevo_usuario.save()
                usuario_a_actualizar = nuevo_usuario

            # Asignar el rol correspondiente (común para ambos casos)
            nuevo_usuario = usuario_a_actualizar
            rol_profesional = Roles.objects.get(nombre_rol=rol_nombre)
            nuevo_usuario.roles.add(rol_profesional)

            # 3. Obtener objetos foráneos
            tipo_id_obj = TipoIdentificacion.objects.get(id_tipo_identificacion=tipo_documento_id)
            genero_obj = Genero.objects.get(id_genero=genero_id)
            centro_medico_obj = CentrosMedicos.objects.get(id_centro_medico=centro_medico_id)
            especialidad_obj = Especialidades.objects.get(id_especialidad=especialidad_id) if especialidad_id else None

            # 4. Crear el perfil del ProfesionalSalud
            ProfesionalSalud.objects.create(
                usuario=nuevo_usuario,
                nombre1=primer_nombre,
                nombre2=segundo_nombre,
                apellido1=primer_apellido,
                apellido2=segundo_apellido,
                id_tipo_identificacion=tipo_id_obj,
                numero_documento=numero_documento,
                id_genero=genero_obj,
                celular=celular,
                correo=email,
                registro_profesional=registro_profesional,
                id_especialidad=especialidad_obj,
                id_centro_medico=centro_medico_obj,
            )
            messages.success(request, f'¡El profesional {primer_nombre} {primer_apellido} ha sido creado con éxito!')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al registrar al profesional: {e}')
        
        return redirect('gestion_admin')
    return redirect('gestion_admin')


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
