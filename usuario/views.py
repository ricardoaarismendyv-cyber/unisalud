from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import uuid
from datetime import timedelta
# Create your views here.
from login.decorators import role_required
from .models import Pacientes, Usuarios, Roles, TipoIdentificacion, Genero, Turnos
from django.contrib import messages
import qrcode
import base64
from io import BytesIO
import uuid
from django.shortcuts import render
from .models import Turnos  # si quieres guardarlo en BD
import string
from django.urls import reverse



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
    return render(request, 'paginas/historia-clinica-usuario.html')

@role_required(allowed_roles=['paciente'])
def omusuario(request):
    return render(request, 'paginas/orden-medica-usuario.html')

@role_required(allowed_roles=['paciente'])
def omeusuario(request):
    return render(request, 'paginas/orden-medicamentos-usuario.html')

# views.py

@role_required(allowed_roles=['paciente'])
def turnosusuario(request):

    # Si ya hay un turno guardado en la sesión
    if request.session.get("turno_id"):
        try:
            turno_existente = Turnos.objects.get(id_turno=request.session["turno_id"])
            
            # Generar el QR del mismo turno
            qr = qrcode.make(turno_existente.solicitud_turno)
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            qr_base64 = base64.b64encode(buffer.getvalue()).decode()

            return render(request, 'paginas/turnos-usuario.html', {
                "turno": turno_existente.solicitud_turno,
                "qr_base64": qr_base64,
            })
        except Turnos.DoesNotExist:
            # Si el turno no existe, continúa para crear uno nuevo
            pass

    # --- Usuario con o sin login ---
    paciente = request.user.paciente if request.user.is_authenticated and hasattr(request.user, "paciente") else None

    # --- Inicializar letra y número ---
    if "letra" not in request.session:
        request.session["letra"] = "A"
    if "numero" not in request.session:
        request.session["numero"] = 1

    letra = request.session["letra"]
    numero = request.session["numero"]

    turno_texto = f"{letra}{numero:03d}"

    # --- Crear turno nuevo ---
    nuevo_turno = Turnos.objects.create(
        id_paciente=paciente,
        id_profesional_id=1,
        id_centro_medico_id=1,
        estado="pendiente",
        fecha_hora_turno=timezone.now(),
        solicitud_turno=turno_texto,
        categoria_turno="General",
        modulo_asignado="Recepción",
        letra=letra,
        numero=numero
    )

    # Guardar ID del turno en sesión (clave principal)
    request.session["turno_id"] = nuevo_turno.id_turno

    # --- Actualizar letra y número siguiente turno ---
    if numero < 999:
        request.session["numero"] += 1
    else:
        import string
        letras = list(string.ascii_uppercase)
        pos = letras.index(letra)
        request.session["letra"] = letras[pos + 1] if pos < 25 else "A"
        request.session["numero"] = 1

    # --- Generar QR del turno ---
    qr = qrcode.make(turno_texto)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'paginas/turnos-usuario.html', {
        "turno": turno_texto,
        "qr_base64": qr_base64,
    })
    




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
    tipos_id = TipoIdentificacion.objects.all()
    generos = Genero.objects.all()
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
