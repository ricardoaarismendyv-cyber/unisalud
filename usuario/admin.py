from django.contrib import admin

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
