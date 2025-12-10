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
        request.session['active_role'] = 'paciente' # <--- AÑADIR ESTA LÍNEA
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
    turno_id_session = request.session.get("turno_id")

    if turno_id_session:
        try:
            turno_existente = Turnos.objects.get(id_turno=turno_id_session)

            if turno_existente.estado != "pendiente":
                del request.session["turno_id"]
            else:
                qr = qrcode.make(turno_existente.solicitud_turno)
                buffer = BytesIO()
                qr.save(buffer, format="PNG")
                qr_base64 = base64.b64encode(buffer.getvalue()).decode()

                return render(request, 'paginas/turnos-usuario.html', {
                    "turno": turno_existente.solicitud_turno,
                    "qr_base64": qr_base64,
                })

        except Turnos.DoesNotExist:
            if "turno_id" in request.session:
                del request.session["turno_id"]

    # ---------- CORRECCIÓN IMPORTANTE ----------
    # Obtener usuario REAL desde tu modelo Usuarios
    from usuario.models import Usuarios, Pacientes
    usuario_real = Usuarios.objects.get(id_usuario=request.session['id_usuario'])

    # Buscar si ya existe paciente
    try:
        paciente = Pacientes.objects.get(usuario=usuario_real)
    except Pacientes.DoesNotExist:
        paciente = None

    # Si no existe paciente, crearlo automáticamente
    if paciente is None:
        paciente = Pacientes.objects.create(
            usuario=usuario_real,
            nombre1=usuario_real.nombre_usuario,  # Temporal
            apellido1="",
            numero_documento="N/A",
            id_tipo_identificacion_id=1,
            id_genero_id=1
        )

    # ---------- Inicializar letra y número ----------
    if "letra" not in request.session:
        request.session["letra"] = "A"
    if "numero" not in request.session:
        request.session["numero"] = 1

    letra = request.session["letra"]
    numero = request.session["numero"]

    turno_texto = f"{letra}{numero:03d}"

    # ---------- Crear nuevo turno ----------
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

    request.session["turno_id"] = nuevo_turno.id_turno

    # ---------- Actualizar letra y número ----------
    if numero < 999:
        request.session["numero"] += 1
    else:
        import string
        letras = list(string.ascii_uppercase)
        pos = letras.index(letra)
        request.session["letra"] = letras[pos + 1] if pos < 25 else "A"
        request.session["numero"] = 1

    # ---------- Generar QR ----------
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

def contactanos(request):
    return render(request, 'paginas/contactanos.html')
