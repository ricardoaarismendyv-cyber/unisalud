from django.contrib import admin
#indica al administrador Django la contraseña segura-hash
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    Afiliacion,
    AntecedentesPaciente,
    CentrosMedicos,
    Ciudad,
    Consulta,
    Departamento,
    DiagnosticoPaciente,
    Enfermedades,
    Eps,
    Especialidades,
    EstadoCivil,
    EstadoOrden,
    EstratoSocioeconomico,
    Genero,
    GrupoRh,
    Incapacidad,
    Medicamentos,
    NivelesAtencion,
    OrdenMedica,
    Pacientes,
    ProfesionalSalud,
    RedesSalud,
    RegionSalud,
    ResultadosLaboratorio,
    Roles,
    Servicios,
    TipoIdentificacion,
    TipoOrden,
    TiposAfiliacion,
    Turnos,
    Usuarios,
)

# Se define una clase Admin: UsuariosAdmin para el modelo Usuarios, con el fin de que el panel administracion sepa que la contraseña no debe mostrarse en texto plano
class UsuariosAdmin(BaseUserAdmin):
    # Campos que se mostrarán en la lista de usuarios, para mejorar la usabilidad en el panel de administración
    list_display = ('nombre_usuario', 'email', 'id_rol')
    # Campos por los que se podrá buscar, para mejorar la usabilidad en el panel de administración
    search_fields = ('nombre_usuario', 'email')
    # Campos que no son editables directamente en el admin (la contraseña se maneja aparte)
    readonly_fields = ()

models_to_register = [
    Afiliacion, AntecedentesPaciente, CentrosMedicos, Ciudad, Consulta, Departamento,
    DiagnosticoPaciente, Enfermedades, Eps, Especialidades, EstadoCivil, EstadoOrden,
    EstratoSocioeconomico, Genero, GrupoRh, Incapacidad, Medicamentos, NivelesAtencion,
    OrdenMedica, Pacientes, ProfesionalSalud, RedesSalud, RegionSalud, ResultadosLaboratorio,
    Roles, Servicios, TipoIdentificacion, TipoOrden, TiposAfiliacion, Turnos,
]
#se retira Usuarios de la lista anterior para evitar registrar el modelo dos veces. Esta se registra una vez con la clase de administracion personalizada
for model in models_to_register:
    admin.site.register(model)

# Registramos el modelo Usuarios usando nuestra clase personalizada
admin.site.register(Usuarios, UsuariosAdmin) #inscribe el modelo Usuarios en el admin de Django con la configuración definida en UsuariosAdmin, es decir Quiero administrar mi modelo Usuarios en el panel de administración, y quiero que uses la configuración personalizada definida en la clase UsuariosAdmin para hacerlo
