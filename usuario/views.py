from django.shortcuts import render, redirect
from login.decorators import role_required
from .models import Pacientes, Usuarios, Roles, TipoIdentificacion, Genero, ProfesionalSalud, CentrosMedicos, Especialidades
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from usuario.models import Consulta, OrdenMedica
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

@role_required(allowed_roles=['paciente'])
def inicio_usuario(request):
    try:
        paciente_id = request.session.get('id_paciente')
        if not paciente_id:
            # Si no hay id_paciente en la sesión, es un error de acceso.
            messages.error(request, 'No tienes permiso para acceder a esta página. Se requiere un perfil de paciente.')
            return redirect('login')
        paciente = Pacientes.objects.get(id_paciente=paciente_id)
        return render(request, 'paginas/inicio-usuario.html', {'paciente': paciente, 'roles': request.session.get('roles', [])})
    except Pacientes.DoesNotExist:
        messages.error(request, 'No se encontró el perfil del paciente.')
        return redirect('login')

@role_required(allowed_roles=['paciente'])
def hcusuario(request):
    # Cambiar de request.user.paciente a usar sesión
    try:
        paciente_id = request.session.get('id_paciente')
        paciente = Pacientes.objects.get(id_paciente=paciente_id) if paciente_id else None
    except Pacientes.DoesNotExist:
        paciente = None
    
    consultas = Consulta.objects.filter(id_paciente=paciente).order_by('-fecha_programada') if paciente else []
    return render(request, 'paginas/historia-clinica-usuario.html', {'consultas': consultas})

@role_required(allowed_roles=['paciente'])
def omusuario(request):
    """
    Vista para que el PACIENTE vea TODAS sus órdenes médicas
    (medicamentos, exámenes, procedimientos).
    """
    try:
        paciente_id = request.session.get('id_paciente')
        if not paciente_id:
            messages.error(request, 'No se encontró tu perfil de paciente.')
            return redirect('login')
        
        paciente = Pacientes.objects.get(id_paciente=paciente_id)
        
        # Obtener TODAS las órdenes del paciente
        ordenes = OrdenMedica.objects.filter(
            id_paciente=paciente
        ).select_related(
            'id_profesional',
            'id_profesional__id_especialidad',
            'id_tipo_orden',
            'id_medicamento',
            'id_servicio',
            'id_estado_orden',
            'id_centro_medico'
        ).order_by('-fecha_emision')
        
        # Orden más reciente
        orden_reciente = ordenes.first() if ordenes.exists() else None
        
        context = {
            'paciente': paciente,
            'ordenes': ordenes,
            'orden_reciente': orden_reciente,
        }
        return render(request, 'paginas/orden-medica-usuario.html', context)
        
    except Pacientes.DoesNotExist:
        messages.error(request, 'No se encontró tu perfil de paciente.')
        return redirect('login')

@role_required(allowed_roles=['paciente'])
def omeusuario(request):
    """
    Vista para que el PACIENTE vea sus órdenes de MEDICAMENTOS.
    Solo muestra órdenes donde id_tipo_orden = 'Medicamentos'.
    """
    try:
        paciente_id = request.session.get('id_paciente')
        if not paciente_id:
            messages.error(request, 'No se encontró tu perfil de paciente.')
            return redirect('login')
        
        paciente = Pacientes.objects.get(id_paciente=paciente_id)
        
        # Obtener órdenes de MEDICAMENTOS del paciente
        ordenes_medicamentos = OrdenMedica.objects.filter(
            id_paciente=paciente,
            id_tipo_orden__nombre_tipo__iexact='medicamentos'  # Solo medicamentos
        ).select_related(
            'id_profesional',
            'id_profesional__id_especialidad',
            'id_medicamento',
            'id_estado_orden',
            'id_centro_medico'
        ).order_by('-fecha_emision')
        
        # Orden más reciente
        orden_reciente = ordenes_medicamentos.first() if ordenes_medicamentos.exists() else None
        
        context = {
            'paciente': paciente,
            'ordenes': ordenes_medicamentos,
            'orden_reciente': orden_reciente,
        }
        return render(request, 'paginas/orden-medicamentos-usuario.html', context)
        
    except Pacientes.DoesNotExist:
        messages.error(request, 'No se encontró tu perfil de paciente.')
        return redirect('login')

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
    """
    Vista para registrar nuevos usuarios: Pacientes o Profesionales de Salud
    """
    # Cargar datos para los <select> del formulario
    tipos_id = TipoIdentificacion.objects.all()
    generos = Genero.objects.all()
    centros_medicos = CentrosMedicos.objects.filter(estado_centro='activa')  # Solo centros activos
    especialidades = Especialidades.objects.all()
    
    context = {
        'tipos_identificacion': tipos_id,
        'generos': generos,
        'centros_medicos': centros_medicos,
        'especialidades': especialidades,
    }
    
    if request.method == 'POST':
        # 1. OBTENER DATOS DEL FORMULARIO
        nombre_usuario = request.POST.get('nombre_usuario')
        email = request.POST.get('email')
        contrasena = request.POST.get('password')
        confirm_contrasena = request.POST.get('confirmPassword')
        tipo_registro = request.POST.get('tipo_registro', 'paciente')  # 'paciente' o 'profesional'

        # Permite rellenar el formulario en caso de error
        context['form_values'] = request.POST

        # 2. VALIDACIONES BÁSICAS
        if contrasena != confirm_contrasena:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'paginas/registro.html', context)

        if Usuarios.objects.filter(nombre_usuario=nombre_usuario).exists():
            messages.error(request, f'El nombre de usuario "{nombre_usuario}" ya está en uso.')
            return render(request, 'paginas/registro.html', context)

        if Usuarios.objects.filter(email=email).exists():
            messages.error(request, f'El correo electrónico "{email}" ya está registrado.')
            return render(request, 'paginas/registro.html', context)

        # 3. CREAR USUARIO Y PERFIL
        try:
            # 3.1 Determinar el rol según tipo de registro
            if tipo_registro == 'profesional':
                rol = Roles.objects.get(nombre_rol='profesional_salud')
            else:
                rol = Roles.objects.get(nombre_rol='paciente')
            
            # 3.2 Crear usuario en tabla usuarios
            nuevo_usuario = Usuarios(
                nombre_usuario=nombre_usuario,
                email=email,
            )
            nuevo_usuario.set_password(contrasena)  # Hashear contraseña
            nuevo_usuario.save()
            nuevo_usuario.roles.add(rol)  # Asignar rol con ManyToMany

            # 3.3 Obtener datos comunes (ForeignKeys)
            tipo_id_obj = TipoIdentificacion.objects.get(id_tipo_identificacion=request.POST.get('tipoDocumento'))
            genero_obj = Genero.objects.get(id_genero=request.POST.get('genero'))

            # 3.4 CREAR PERFIL SEGÚN TIPO
            if tipo_registro == 'profesional':
                # === CREAR PROFESIONAL DE SALUD ===
                
                # Validar centro médico (OBLIGATORIO)
                centro_medico_id = request.POST.get('centroMedico')
                if not centro_medico_id:
                    messages.error(request, 'Debe seleccionar un centro médico.')
                    nuevo_usuario.delete()  # Eliminar usuario huérfano
                    return render(request, 'paginas/registro.html', context)
                
                centro_obj = CentrosMedicos.objects.get(id_centro_medico=centro_medico_id)
                
                # Especialidad (OPCIONAL)
                especialidad_id = request.POST.get('especialidad')
                especialidad_obj = Especialidades.objects.get(id_especialidad=especialidad_id) if especialidad_id else None
                
                # Crear el perfil profesional
                ProfesionalSalud.objects.create(
                    usuario=nuevo_usuario,
                    numero_documento=request.POST.get('numeroDocumento'),
                    nombre1=request.POST.get('primerNombre'),
                    nombre2=request.POST.get('segundoNombre') or None,  # Manejar vacío como None
                    apellido1=request.POST.get('primerApellido'),
                    apellido2=request.POST.get('segundoApellido') or None,
                    id_tipo_identificacion=tipo_id_obj,
                    id_genero=genero_obj,
                    fecha_nacimiento=request.POST.get('fechaNacimiento') or None,
                    telefono=request.POST.get('telefono') or None,
                    celular=request.POST.get('celular') or None,
                    correo=email,
                    registro_profesional=request.POST.get('registroProfesional') or None,  # Opcional
                    id_especialidad=especialidad_obj,
                    id_centro_medico=centro_obj,  # OBLIGATORIO
                    estado='activo'
                )
                
            else:
                # === CREAR PACIENTE (código existente) ===
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
                    direccion=request.POST.get('direccion'),
                    telefono=request.POST.get('telefono'),    
                    celular=request.POST.get('celular'),
                    correo_electronico=email 
                )

            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('login')

        except Roles.DoesNotExist:
            messages.error(request, f'El rol "{tipo_registro}" no está configurado. Contacta al administrador.')
            return render(request, 'paginas/registro.html', context)
        except CentrosMedicos.DoesNotExist:
            messages.error(request, 'El centro médico seleccionado no existe.')
            if 'nuevo_usuario' in locals() and nuevo_usuario.pk:
                nuevo_usuario.delete()
            return render(request, 'paginas/registro.html', context)
        except Exception as e:
            messages.error(request, f'Ocurrió un error inesperado: {e}')
            if 'nuevo_usuario' in locals() and nuevo_usuario.pk:
                nuevo_usuario.delete()
            return render(request, 'paginas/registro.html', context)

    return render(request, 'paginas/registro.html', context)

def contactanos(request):
    return render(request, 'paginas/contactanos.html')

@role_required(allowed_roles=['paciente'])
def descargar_pdf_orden_paciente(request, id_orden):
    """
    Permite al PACIENTE descargar el PDF de su orden médica desde PostgreSQL.
    """
    try:
        paciente_id = request.session.get('id_paciente')
        if not paciente_id:
            messages.error(request, 'No se encontró tu perfil de paciente.')
            return redirect('login')
        
        paciente = Pacientes.objects.get(id_paciente=paciente_id)
        
        # Obtener la orden (verificar que pertenezca al paciente)
        orden = get_object_or_404(OrdenMedica, id_orden=id_orden, id_paciente=paciente)
        
        # Obtener PDF desde PostgreSQL
        pdf_bytes = orden.get_pdf_from_db()
        
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="orden_{orden.id_orden}.pdf"'
        return response
        
    except Pacientes.DoesNotExist:
        messages.error(request, 'No se encontró tu perfil de paciente.')
        return redirect('login')
