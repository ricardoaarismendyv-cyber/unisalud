from django.shortcuts import render, redirect
from login.decorators import role_required
from django.contrib import messages
from usuario.models import TipoIdentificacion, Genero, Pacientes, Usuarios, Roles, ProfesionalSalud, CentrosMedicos  # Importar modelos necesarios
from django.contrib.auth.hashers import make_password # Para encriptar la contraseña
import qrcode
import base64
from io import BytesIO
import uuid
from django.shortcuts import render
from usuario.models import Turnos
import string

# Create your views here.
ALLOWED_ADMIN_ROLES = ['admin_centro_medico']

def login_admin(request):
    return render(request, 'paginas/login_admin.html')

@role_required(allowed_roles=ALLOWED_ADMIN_ROLES)
def inicio_admin(request):
    return render(request, 'paginas/inicio_admin.html')

def gestion_admin(request):
    # 1. Consultar la base de datos para obtener los datos necesarios
    tipos_id = TipoIdentificacion.objects.all()
    generos = Genero.objects.all()
    centros_medicos = CentrosMedicos.objects.all()
    # 2. Crear un diccionario de contexto para pasar los datos a la plantilla
    context = {'tipos_identificacion': tipos_id, 'generos': generos, 'centros_medicos': centros_medicos}
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
            direccion = request.POST.get('direccion', '')
            telefono = request.POST.get('telefono', '')
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


# views.py# si quieres guardarlo en BD

def turnos_admin(request):
    return render(request, 'paginas/turnos_admin.html')
    request.session['active_role'] = 'admin_centro_medico' # <--- AÑADIR ESTA LÍNEA
    # Aquí puedes añadir lógica para buscar el perfil del admin si es necesario
    return render(request, 'paginas/inicio_admin.html', {'roles': request.session.get('roles', [])})
    # Generar el siguiente turno ordenado
    turno_obj = generar_turno()
    turno = f"{turno_obj.letra}{turno_obj.numero:03d}"

    # Crear QR
    qr = qrcode.make(turno)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'paginas/turnos-usuario.html', {
        "turno": turno,
        "qr_base64": qr_base64
    })

# utils.py
import string
from usuario.models import Turnos

def generar_turno():
    # Si no hay turnos previos, comenzar en A001
    ultimo = Turnos.objects.order_by('-id').first()

    if not ultimo:
        return Turnos.objects.create(letra="A", numero=1)

    letra = ultimo.letra
    numero = ultimo.numero

    # Si el número llega a 999 → pasar a siguiente letra
    if numero >= 999:
        letras = list(string.ascii_uppercase)
        pos = letras.index(letra)

        # Si llega a Z999 → reiniciar A001
        if pos == len(letras) - 1:
            letra = "A"
        else:
            letra = letras[pos + 1]

        numero = 1
    else:
        numero += 1

    return Turnos.objects.create(letra=letra, numero=numero)
