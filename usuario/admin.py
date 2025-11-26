from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm # Formularios que heredan de los formularios base de Django, estos formularios piden la contraseña dos veces para confirmarla y manejan el hasheo de la contraseña automáticamente
from django import forms
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

# se usan formularios personalizados para manejar la creación de usuarios y el hasheo de contraseñas
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuarios
        fields = ('nombre_usuario', 'email', 'roles')
# # Formularios que heredan de los formularios base de Django, estos formularios piden la contraseña dos veces para confirmarla y manejan el hasheo de la contraseña automáticamente
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Usuarios
        fields = ('nombre_usuario', 'email', 'roles')

class UsuariosAdmin(admin.ModelAdmin):
    # Formularios para creación y edición de usuarios en el panel administrativo
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # Campos a mostrar en la lista
    list_display = ('nombre_usuario', 'email', 'roles')
    # Campos para búsqueda
    search_fields = ('nombre_usuario', 'email')
    # Filtros en la barra lateral
    list_filter = ('roles',)
    
    # Define los campos que se mostrarán en el formulario de creación/edición
    # La contraseña no se incluye aquí porque los formularios base la manejan por separado
    fieldsets = (
        (None, {'fields': ('nombre_usuario', 'email', 'roles')}),
    )
    add_fieldsets = (
        (None, {'fields': ('nombre_usuario', 'email', 'roles', 'password', 'password2')}),
    )

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
# admin.site.register(Usuarios, UsuariosAdmin) #inscribe el modelo Usuarios en el admin de Django con la configuración definida en UsuariosAdmin, es decir Quiero administrar mi modelo Usuarios en el panel de administración, y quiero que uses la configuración personalizada definida en la clase UsuariosAdmin para hacerlo
