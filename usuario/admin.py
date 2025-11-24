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
# Register your models here.

models_to_register = [
    Afiliacion, AntecedentesPaciente, CentrosMedicos, Ciudad, Consulta, Departamento,
    DiagnosticoPaciente, Enfermedades, Eps, Especialidades, EstadoCivil, EstadoOrden,
    EstratoSocioeconomico, Genero, GrupoRh, Incapacidad, Medicamentos, NivelesAtencion,
    OrdenMedica, Pacientes, ProfesionalSalud, RedesSalud, RegionSalud, ResultadosLaboratorio,
    Roles, Servicios, TipoIdentificacion, TipoOrden, TiposAfiliacion, Turnos, Usuarios,
]

for model in models_to_register:
    admin.site.register(model)

# Registramos el modelo Usuarios usando nuestra clase personalizada
admin.site.register(Usuarios, UsuariosAdmin)
