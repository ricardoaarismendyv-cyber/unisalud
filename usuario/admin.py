from django.contrib import admin

from .models import (
    afiliacion,
    antecedentespaciente,
    centrosmedicos,
    ciudad,
    consulta,
    departamento,
    detallemedicamento,
    diagnosticopaciente,
    enfermedades,
    eps,
    especialidades,
    estadocivil,
    estadoorden,
    estratosocioeconomico,
    genero,
    gruporh,
    incapacidad,
    medicamentos,
    nivelesatencion,
    ordenmedica,
    pacientes,
    profesionalsalud, # Mantener este si es el nombre correcto de la clase
    redessalud,
    regionsalud,
    resultadoslaboratorio,
    Roles,
    servicios,
    tipoidentificacion,
    tipoorden,
    tiposafiliacion,
    turnos,
    Usuarios,
)
# Register your models here.

models_to_register = [
    afiliacion, antecedentespaciente, centrosmedicos, ciudad, consulta, departamento,
    detallemedicamento, diagnosticopaciente, enfermedades, eps, especialidades,
    estadocivil, estadoorden, estratosocioeconomico, genero, gruporh, incapacidad, # Mantener estos si son los nombres correctos
    medicamentos, nivelesatencion, ordenmedica, pacientes, profesionalsalud, # Mantener estos si son los nombres correctos
    redessalud, regionsalud, resultadoslaboratorio, Roles, servicios, # Mantener estos si son los nombres correctos
    tipoidentificacion, tipoorden, tiposafiliacion, turnos, Usuarios
]

for model in models_to_register:
    admin.site.register(model)
