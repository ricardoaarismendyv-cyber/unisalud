from django.contrib import admin
<<<<<<< Updated upstream

# Register your models here.
=======
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
    profesionalsalud,
    redessalud,
    regionsalud,
    resultadoslaboratorio,
    roles,
    servicios,
    tipoidentificacion,
    tipoorden,
    tiposafiliacion,
    turnos,
    usuarios,
)
# Register your models here.

models_to_register = [
    afiliacion, antecedentespaciente, centrosmedicos, ciudad, consulta, departamento,
    detallemedicamento, diagnosticopaciente, enfermedades, eps, especialidades,
    estadocivil, estadoorden, estratosocioeconomico, genero, gruporh, incapacidad,
    medicamentos, nivelesatencion, ordenmedica, pacientes, profesionalsalud,
    redessalud, regionsalud, resultadoslaboratorio, roles, servicios,
    tipoidentificacion, tipoorden, tiposafiliacion, turnos, usuarios
]

for model in models_to_register:
    admin.site.register(model)
>>>>>>> Stashed changes
