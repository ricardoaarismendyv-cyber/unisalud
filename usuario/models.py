from django.db import models
from django.contrib.auth.hashers import make_password, check_password #para codificar y verificar las contraseñas de forma segura
from django.core.files.base import ContentFile
import qrcode
from io import BytesIO
# aqui cambio los nombres de las clases a tipo CamelCase (nombre pegado con cada primera letra de la palabra en mayuscula)
#cambio las tablas de db_table a su respectivo en minuscula y un guion bajo
#cambio las foreignKey para que usen la class adecuada
#se elimina la class DetallesMedicamento
class Roles(models.Model): 
    id_rol = models.AutoField(primary_key=True, db_comment='ID autoincremental del roles')
    nombre_rol = models.CharField(unique=True, max_length=50, db_comment='Nombre de los roles: paciente, profesional_salud, laboratorista, recepcionista, admin_centro_medico, turnero')
    descripcion = models.TextField(blank=True, null=True, db_comment='Descripcion de los roles para mayor claridad, opcional')

    class Meta:
        managed = True
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.nombre_rol

#en roles me sale error de: manytomanyfield 'Usuarios.roles', es decir, Django te está diciendo: "He visto que has puesto un comentario aquí, pero no sé dónde ponerlo en la base de datos para este tipo de campo, así que lo voy a ignorar".
#para ello se elimina el parámetro db_comment en el ManyToManyField de Roles en la clase Usuarios
class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True, db_comment='ID autoincremental del usuario')
    roles = models.ManyToManyField('Roles', db_comment='Roles asignados para pacientes, profesional salud, recepcionista, laboratorista, adm centro, turnero')
    nombre_usuario = models.CharField(unique=True, max_length=50, db_comment='Login unico para el usuario')
    contrasena = models.CharField(max_length=255, db_comment='Contrasena que crea el usuario')
    email = models.CharField(unique=True, max_length=100, blank=True, null=True, db_comment='Correo principal-login del usuario')
    
    class Meta:
        managed = True
        db_table = 'usuarios'

    def __str__(self):
        return self.nombre_usuario

#manejar contraseñas de forma segura
#set_password: toma la contraseña en texto plano y la codifica antes de almacenarla en la base de datos.
    def set_password(self, raw_password):
        self.contrasena = make_password(raw_password)

#check_password: verifica si la contraseña en texto plano coincide con la contraseña codificada almacenada.
    def check_password(self, raw_password):
        return check_password(raw_password, self.contrasena)

class TipoIdentificacion(models.Model):
    id_tipo_identificacion = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    identificacion = models.CharField(unique=True, max_length=50, db_comment='Abreviatura del tipo de identificacion: CC, TI, etc')
    nombre_identificacion = models.CharField(max_length=50, db_comment='Nombre completo del tipo de identificacion: Cédula de Ciudadanía, Tarjeta de Identidad, etc')
    descripcion = models.TextField(blank=True, null=True, db_comment='Descripcion opcional')

    class Meta:
        managed = True
        db_table = 'tipo_identificacion'
        verbose_name = 'Tipo de Identificacion'
        verbose_name_plural = 'Tipos de Identificacion'

    def __str__(self):
        return self.nombre_identificacion


class Genero(models.Model):
    id_genero = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_genero = models.CharField(unique=True, max_length=20, db_comment='Ej: Masculino, Femenino, No Binario, etc')

    
    def __str__(self):
        return self.nombre_genero
    
    class Meta:
        managed = True
        db_table = 'genero'


class GrupoRh(models.Model):
    id_rh = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    tipo_rh = models.CharField(unique=True, max_length=3, db_comment='Ej: A+, B-, etc')

    
    def __str__(self):
        return self.tipo_rh
    
    class Meta:
        managed = True
        db_table = 'grupo_rh'


class EstadoCivil(models.Model):
    id_estado_civil = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_estado = models.CharField(unique=True, max_length=20, db_comment='Ej: soltero, casado, etc')

    class Meta:
        managed = True
        db_table = 'estado_civil'

    def __str__(self):
        return self.nombre_estado


class EstratoSocioeconomico(models.Model):
    id_estrato = models.IntegerField(primary_key=True, db_comment='ID del 1 al 6')
    descripcion = models.CharField(max_length=100, db_comment='Ej: Bajo, Medio, alto')

    class Meta:
        managed = True
        db_table = 'estrato_socioeconomico'

    def __str__(self):
        return f'Estrato {self.id_estrato}'


class RegionSalud(models.Model):
    id_region = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_region = models.CharField(unique=True, max_length=100, db_comment='Nombre de la region Ej: caribe, eje cafetero, sur occidente, etc')
    descripcion = models.TextField(blank=True, null=True, db_comment='Descripcion')

    class Meta:
        managed = True
        db_table = 'region_salud'

    def __str__(self):
        return self.nombre_region


class Departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_departamento = models.CharField(max_length=100, db_comment='Nombre del departamento')
    id_region = models.ForeignKey('RegionSalud', models.DO_NOTHING, db_column='id_region', blank=True, null=True, db_comment='Referencia a REGION_SALUD')
    codigo_dane = models.CharField(max_length=10, blank=True, null=True, db_comment='Codigo DANE para identificar oficialmente c-depto.')

    class Meta:
        managed = True
        db_table = 'departamento'

    def __str__(self):
        return self.nombre_departamento


class Ciudad(models.Model):
    id_ciudad = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_ciudad = models.CharField(max_length=100, db_comment='Nombre de la ciudad')
    id_departamento = models.ForeignKey('Departamento', models.DO_NOTHING, db_column='id_departamento', db_comment='Referencia a DEPARTAMENTO')
    codigo_dane = models.CharField(max_length=10, blank=True, null=True, db_comment='Codigo DANE para identificar oficialmente c-ciudad')

    class Meta:
        managed = True
        db_table = 'ciudad'

    def __str__(self):
        return self.nombre_ciudad


class RedesSalud(models.Model):
    id_red = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_red = models.CharField(unique=True, max_length=150, db_comment='Nombre de la red: RIPSS (Redes integrales de prestadores de servicios de salud)')
    descripcion = models.TextField(blank=True, null=True, db_comment='Descripcion')
    id_region = models.ForeignKey('RegionSalud', models.DO_NOTHING, db_column='id_region', blank=True, null=True, db_comment='Referencia a REGION_SALUD')
    estado_red = models.CharField(max_length=8, blank=True, null=True, db_comment='Esta activa, inactiva')

    class Meta:
        managed = True
        db_table = 'redes_salud'

    def __str__(self):
        return self.nombre_red


class NivelesAtencion(models.Model):
    id_nivel = models.IntegerField(primary_key=True, db_comment='ID del nivel (1 a 3)')
    nombre_nivel = models.CharField(max_length=50, db_comment='de acuerdo al grado de complejidad en salud: primer nivel-atencion basica')
    descripcion = models.TextField(blank=True, null=True, db_comment='Descripcion')

    class Meta:
        managed = True
        db_table = 'niveles_atencion'

    def __str__(self):
        return self.nombre_nivel


class CentrosMedicos(models.Model):
    id_centro_medico = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_centro = models.CharField(max_length=150, db_comment='Nombre del centro medico')
    id_red_salud = models.ForeignKey('RedesSalud', models.DO_NOTHING, db_column='id_red_salud', blank=True, null=True, db_comment='Referencia a redessalud')
    id_nivel_atencion = models.ForeignKey('NivelesAtencion', models.DO_NOTHING, db_column='id_nivel_atencion', null=True, db_comment='Referencia a NIVELES_ATENCION')
    id_ciudad = models.ForeignKey('Ciudad', models.DO_NOTHING, db_column='id_ciudad', null=True, db_comment='Referencia a CIUDAD')
    direccion = models.CharField(max_length=255, db_comment='Direccion centro medico')
    celular = models.CharField(max_length=60, blank=True, null=True, db_comment='Celular centro medico')
    telefono = models.CharField(max_length=60, blank=True, null=True, db_comment='Telefono centro medico')
    correo = models.CharField(max_length=100, blank=True, null=True, db_comment='Correo entro medico')
    
    class Meta:
        managed = True
        db_table = 'centros_medicos'

    def __str__(self):
        return self.nombre_centro


class Eps(models.Model):
    id_eps = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_eps = models.CharField(unique=True, max_length=100, db_comment='Nombre de la EPS')
    nit = models.CharField(max_length=20, blank=True, null=True, db_comment='NIT de la EPS')
    direccion = models.CharField(max_length=255, blank=True, null=True, db_comment='Direccion de la EPS')
    telefono = models.CharField(max_length=15, blank=True, null=True, db_comment='Telefono de la EPS')
    correo = models.CharField(max_length=100, blank=True, null=True, db_comment='Correo de la EPS')
    estado_eps = models.CharField(max_length=8, blank=True, null=True, db_comment='Esta activa, inactiva')

    class Meta:
        managed = True
        db_table = 'eps'

    def __str__(self):
        return self.nombre_eps


class TiposAfiliacion(models.Model):
    id_tipo_afiliacion = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_tipo = models.CharField(unique=True, max_length=20, db_comment='el paciente esta en regimen Contributivo, Subsidiado, etc')

    class Meta:
        managed = True
        db_table = 'tipos_afiliacion'

    def __str__(self):
        return self.nombre_tipo


class Especialidades(models.Model):
    id_especialidad = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    codigo_especialidad = models.IntegerField(default=0, db_comment='Codigo unico para la especialidad medica')
    nombre_especialidad = models.CharField(unique=True, max_length=100, db_comment='refiere a la especialidad medica: neurologia, cardiologia, etc')
    descripcion = models.TextField(blank=True, null=True, db_comment='Descripcion')

    class Meta:
        managed = True
        db_table = 'especialidades'

    def __str__(self):
        return self.nombre_especialidad


class Medicamentos(models.Model):
    id_medicamento = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    codigo_medicamento = models.IntegerField(default=0, db_comment='Codigo unico del medicamento')
    nombre_generico = models.CharField(max_length=200, blank=True, null=True, db_comment='Nombre generico medicamento')
    principio_activo = models.CharField(max_length=500, blank=True, null=True, db_comment='Principio activo medicamento')
    concentracion = models.CharField(max_length=350, blank=True, null=True, db_comment='Concentracion medicamento')
    forma_farmaceutica = models.CharField(max_length=350, blank=True, null=True, db_comment='Forma farmaceutica medicamento')
    registro_invima = models.CharField(unique=True, max_length=500, db_comment='Registro INVIMA del medicamento')
    
    class Meta:
        managed = True
        db_table = 'medicamentos'

    def __str__(self):
        return self.nombre_generico


class Servicios(models.Model):
    id_servicio = models.AutoField(primary_key=True, db_comment='ID autoincremental del servicio')
    codigo_servicio = models.IntegerField(default=0, db_comment='Codigo unico del servicio medico')
    nombre_servicio = models.CharField(max_length=500, db_comment='Nombre del servicio medico')
    tipo_servicio = models.CharField(max_length=550, db_comment='Categoria: imagenologia, laboratorio, etc')
    id_especialidad = models.ForeignKey('Especialidades', models.DO_NOTHING, db_column='id_especialidad', blank=True, null=True, db_comment='Especialidad requerida (opcional)')

    class Meta:
        managed = True
        db_table = 'servicios'

    def __str__(self):
        return self.nombre_servicio


class Enfermedades(models.Model):
    id_enfermedad = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    codigo_cie10 = models.CharField(max_length=300, unique=True, db_comment='Codigo CIE-10 para clasificar diagnosticos, sintomas')
    nombre_enfermedad = models.CharField(max_length=300, db_comment='Nombre de la enfermedad')
    descripcion = models.TextField(blank=True, null=True, db_comment='Descripcion clinica de la enfermedad')
    categoria_grupom = models.CharField(max_length=300, blank=True, null=True, db_comment='refiere al grupo de mortalidad CIE10')
    grupo_mortalidad = models.CharField(max_length=250, blank=True, null=True, db_comment='de acuerdo con la CIE-10 ')

    class Meta:
        managed = True
        db_table = 'enfermedades'

    def __str__(self):
        return f'{self.codigo_cie10} - {self.nombre_enfermedad}'


class EstadoOrden(models.Model):
    id_estado_orden = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_estado_orden = models.CharField(unique=True, max_length=20, db_comment='esta: pendiente, entregada, etc')

    class Meta:
        managed = True
        db_table = 'estado_orden'

    def __str__(self):
        return self.nombre_estado_orden


class TipoOrden(models.Model):
    id_tipo = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_tipo = models.CharField(unique=True, max_length=50, db_comment='Es: Medicamentos, examenes, etc')

    class Meta:
        managed = True
        db_table = 'tipo_orden'

    def __str__(self):
        return self.nombre_tipo


class Pacientes(models.Model):
    id_paciente = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    usuario = models.OneToOneField('Usuarios', on_delete=models.CASCADE, related_name='paciente', blank=True, null=True, db_comment='Referencia a la cuenta de USUARIOS')
    id_tipo_identificacion = models.ForeignKey('TipoIdentificacion', models.DO_NOTHING, db_column='id_tipo_identificacion', db_comment='Referencia a TIPO_IDENTIFICACION')
    numero_documento = models.CharField(max_length=20, db_comment='Numero del documento paciente')
    nombre1 = models.CharField(max_length=50, db_comment='Primer nombre paciente')
    nombre2 = models.CharField(max_length=50, blank=True, null=True, db_comment='Segundo nombre paciente, opcional')
    apellido1 = models.CharField(max_length=50, db_comment='Primer apellido paciente')
    apellido2 = models.CharField(max_length=50, blank=True, null=True, db_comment='Segundo apellido paciente, opcional')
    id_genero = models.ForeignKey('Genero', models.DO_NOTHING, db_column='id_genero', db_comment='Referencia a GENERO')
    id_rh = models.ForeignKey('GrupoRh', models.DO_NOTHING, db_column='id_rh', blank=True, null=True, db_comment='Referencia a GRUPO_RH')
    fecha_nacimiento = models.DateField(db_comment='Fecha de nacimiento paciente')
    id_estado_civil = models.ForeignKey('EstadoCivil', models.DO_NOTHING, db_column='id_estado_civil', blank=True, null=True, db_comment='Referencia a ESTADO_CIVIL')
    id_estrato = models.ForeignKey('EstratoSocioeconomico', models.DO_NOTHING, db_column='id_estrato', blank=True, null=True, db_comment='Referencia a ESTRATO')
    direccion = models.CharField(max_length=255, blank=True, null=True, db_comment='Direccion paciente')
    celular = models.CharField(max_length=15, blank=True, null=True, db_comment='Celular paciente')
    telefono = models.CharField(max_length=15, blank=True, null=True, db_comment='Telefono fijo paciente, opcional')
    correo_electronico = models.CharField(max_length=100, blank=True, null=True, db_comment='Correo paciente, opcional')
    fecha_registro = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_comment='Fecha de registro paciente')

    class Meta:
        managed = True
        db_table = 'pacientes'
        unique_together = (('id_tipo_identificacion', 'numero_documento'),)

    def __str__(self):
        return f'{self.nombre1} {self.apellido1}'


class ProfesionalSalud(models.Model):
    id_profesional = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    usuario = models.OneToOneField('Usuarios', on_delete=models.CASCADE, related_name='profesional_salud', db_comment='Referencia a la cuenta de USUARIOS (Obligatorio para personal)')
    id_tipo_identificacion = models.ForeignKey('TipoIdentificacion', models.DO_NOTHING, db_column='id_tipo_identificacion', db_comment='Referencia a TIPO_IDENTIFICACION')
    numero_documento = models.CharField(max_length=20, db_comment='Numero del documento profesional salud')
    nombre1 = models.CharField(max_length=50, db_comment='Primer nombre profesional salud')
    nombre2 = models.CharField(max_length=50, blank=True, null=True, db_comment='Segundo nombre profesional salud')
    apellido1 = models.CharField(max_length=50, db_comment='Primer apellido profesional salud')
    apellido2 = models.CharField(max_length=50, blank=True, null=True, db_comment='Segundo apellido profesional salud')
    id_genero = models.ForeignKey('Genero', models.DO_NOTHING, db_column='id_genero', db_comment='Referencia a GENERO')
    fecha_nacimiento = models.DateField(blank=True, null=True, db_comment='Fecha de nacimiento profesional salud')
    telefono = models.CharField(max_length=15, blank=True, null=True, db_comment='Telefono profesional salud, opcional')
    celular = models.CharField(max_length=15, blank=True, null=True, db_comment='Celular profesional salud')
    correo = models.CharField(max_length=100, blank=True, null=True, db_comment='Correo profesional salud')
    registro_profesional = models.CharField(unique=True, max_length=50, blank=True, null=True, db_comment='Registro medico, puede ser NULL para recepcionistas-admins')
    id_especialidad = models.ForeignKey('Especialidades', models.DO_NOTHING, db_column='id_especialidad', blank=True, null=True, db_comment='Referencia a ESPECIALIDADES')
    id_centro_medico = models.ForeignKey('CentrosMedicos', models.DO_NOTHING, db_column='id_centro_medico', db_comment='Centro medico donde trabaja (Obligatorio)')
    fecha_vinculacion = models.DateField(blank=True, null=True, db_comment='Fecha de vinculacion')
    estado = models.CharField(max_length=10, blank=True, null=True, db_comment='Esta: activo, inactivo, etc')

    class Meta:
        managed = True
        db_table = 'profesional_salud'
        unique_together = (('id_tipo_identificacion', 'numero_documento'),)
        verbose_name = 'Profesional de Salud'
        verbose_name_plural = 'Profesionales de Salud'

    def __str__(self):
        return f'{self.nombre1} {self.apellido1}'


class Afiliacion(models.Model):
    id_afiliacion = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    id_paciente = models.ForeignKey('Pacientes', models.DO_NOTHING, db_column='id_paciente', db_comment='Referencia a PACIENTES')
    id_eps = models.ForeignKey('Eps', models.DO_NOTHING, db_column='id_eps', db_comment='Referencia a EPS')
    id_tipo_afiliacion = models.ForeignKey('TiposAfiliacion', models.DO_NOTHING, db_column='id_tipo_afiliacion', db_comment='Referencia a TIPOS_AFILIACION')
    fecha_inicio = models.DateField(db_comment='Fecha de inicio afliacion')
    fecha_fin = models.DateField(blank=True, null=True, db_comment='Fecha de fin de la afiliacion')
    estado_afiliacion = models.CharField(max_length=10, blank=True, null=True, db_comment='Esta: activo, inactiva')

    class Meta:
        managed = True
        db_table = 'afiliacion'

    def __str__(self):
        return f'Afiliación de {self.id_paciente} a {self.id_eps}'
    

class Consulta(models.Model):
    id_consulta = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    id_paciente = models.ForeignKey('Pacientes', models.DO_NOTHING, db_column='id_paciente', db_comment='Referencia a PACIENTES')
    id_profesional = models.ForeignKey('ProfesionalSalud', models.DO_NOTHING, db_column='id_profesional', db_comment='Referencia a PROFESIONAL_SALUD')
    id_centro_medico = models.ForeignKey('CentrosMedicos', models.DO_NOTHING, db_column='id_centro_medico', db_comment='Referencia a CENTROS_MEDICOS')
    estado = models.CharField(max_length=10, blank=True, null=True, db_comment='Esta: programada, atendido, etc')
    fecha_programada = models.DateTimeField(db_comment='Fecha programada la consulta')
    fecha_atencion = models.DateTimeField(blank=True, null=True, db_comment='Fecha de atencion consulta')
    motivo_consulta = models.TextField(blank=True, null=True, db_comment='Motivo por la que el paciente asiste a la consulta')
    anamnesis = models.TextField(blank=True, null=True, db_comment='informacion que aporta el paciente para crear el historial clinico')
    examen_fisico = models.TextField(blank=True, null=True, db_comment='Examen fisico, exploratorio al paciente')
    frecuencia_cardiaca = models.IntegerField(blank=True, null=True, db_comment='FC en lpm')
    frecuencia_respiratoria = models.IntegerField(blank=True, null=True, db_comment='FR en rpm')
    temperatura = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, db_comment='Temperatura en grados C')
    saturacion_oxigeno = models.IntegerField(blank=True, null=True, db_comment='SpO2 en porcentaje')
    presion_arterial_sistolica = models.IntegerField(blank=True, null=True, db_comment='TA sistolica')
    presion_arterial_diastolica = models.IntegerField(blank=True, null=True, db_comment='TA diastolica')
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, db_comment='Peso en kg')
    talla = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, db_comment='Talla en cm')
    imc = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, db_comment='Indice de Masa Corporal')
    habitos_fumador = models.CharField(max_length=9, blank=True, null=True, db_comment='Fuma')
    habitos_alcohol = models.CharField(max_length=9, blank=True, null=True, db_comment='Consume alcohol')
    habitos_ejercicio = models.CharField(max_length=2, blank=True, null=True, db_comment='Realiza actividad fisica')
    revision_sistemas = models.TextField(blank=True, null=True, db_comment='Revision por sistemas')
    impresion_diagnostica = models.TextField(blank=True, null=True, db_comment='Diagnostico al paciente')
    plan_tratamiento = models.TextField(blank=True, null=True, db_comment='Plan de tratamiento para el paciente')
    notas_adicionales = models.TextField(blank=True, null=True, db_comment='Notas del profesional salud, opcional')
    creado_en = models.DateTimeField(blank=True, null=True, db_comment='Fecha de registro de la consulta')

    class Meta:
        managed = True
        db_table = 'consulta'
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'

    def __str__(self):
        return f'Consulta {self.id_consulta} - {self.id_paciente}'


class OrdenMedica(models.Model):
    id_orden = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    id_paciente = models.ForeignKey('Pacientes', on_delete=models.CASCADE, db_column='id_paciente', db_comment='Referencia a PACIENTE')
    id_profesional = models.ForeignKey('ProfesionalSalud', on_delete=models.CASCADE, db_column='id_profesional', db_comment='Referencia a PROFESIONAL_SALUD')
    id_medicamento = models.ForeignKey('Medicamentos', on_delete=models.CASCADE, db_column='id_medicamento', null=True, blank=True, db_comment='Referencia a MEDICAMENTO')
    id_tipo_orden = models.ForeignKey('TipoOrden', on_delete=models.CASCADE, db_column='id_tipo_orden', db_comment='Referencia a TIPO_ORDEN')
    id_servicio = models.ForeignKey('Servicios', on_delete=models.CASCADE, db_column='id_servicio', null=True, blank=True, db_comment='Referencia a SERVICIOS')
    dosis = models.CharField(max_length=100, null=True, blank=True, db_comment='Dosis del medicamento')
    duracion_tratamiento = models.CharField(max_length=100, null=True, blank=True, db_comment='De acuerdo al diagnostico')
    frecuencia = models.CharField(max_length=50, null=True, blank=True, db_comment='Frecuencia de acuerdo al diagnostico')
    cantidad = models.IntegerField(null=True, blank=True, db_comment='Cantidad de acuerdo al diagnostico')
    indicaciones = models.TextField(null=True, blank=True, db_comment='Indicaciones tratamiento y-o procedimiento')
    id_centro_medico = models.ForeignKey('CentrosMedicos', models.DO_NOTHING, db_column='id_centro_medico', db_comment='Centro medico donde se emite')
    id_estado_orden = models.ForeignKey('EstadoOrden', models.DO_NOTHING, db_column='id_estado_orden', db_comment='Referencia a ESTADO_ORDEN')
    fecha_emision = models.DateTimeField(blank=True, null=True, db_comment='Fecha de emision de la orden')
    fecha_cumplimiento = models.DateTimeField(blank=True, null=True, db_comment='Fecha de cumplimiento, maximo 30 dias')
    codigo_qr = models.CharField(max_length=255, blank=True, null=True, db_comment='Codigo QR para descarga segura')
    id_consulta = models.ForeignKey('Consulta', models.DO_NOTHING, db_column='id_consulta', blank=True, null=True, db_comment='Referencia opcional a CONSULTA')

    class Meta:
        managed = True
        db_table = 'orden_medica'
        verbose_name = 'Orden Medica'
        verbose_name_plural = 'Ordenes Medicas'

    def __str__(self):
        return f'Orden {self.id_orden} - {self.id_paciente}'


class DiagnosticoPaciente(models.Model):
    id_diagnostico = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    id_consulta = models.ForeignKey('Consulta', models.DO_NOTHING, db_column='id_consulta', db_comment='Referencia a CONSULTA')
    id_enfermedad = models.ForeignKey('Enfermedades', models.DO_NOTHING, db_column='id_enfermedad', db_comment='Referencia a ENFERMEDADES')
    tipo_diagnostico = models.CharField(max_length=10, blank=True, null=True, db_comment='Es: presuntivo, principal, etc')
    notas = models.TextField(blank=True, null=True, db_comment='Notas')
    fecha_registro = models.DateTimeField(blank=True, null=True, db_comment='Fecha de registro')

    class Meta:
        managed = True
        db_table = 'diagnostico_paciente'

    def __str__(self):
        return f'Diagnóstico para consulta {self.id_consulta}: {self.id_enfermedad}'


class Turnos(models.Model):
    id_turno = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    id_paciente = models.ForeignKey('Pacientes', models.SET_NULL, db_column='id_paciente', null=True, blank=True, db_comment='Referencia a PACIENTES')
    id_profesional = models.ForeignKey('ProfesionalSalud', models.DO_NOTHING, db_column='id_profesional', db_comment='Referencia a PROFESIONAL_SALUD')
    id_centro_medico = models.ForeignKey('CentrosMedicos', models.DO_NOTHING, db_column='id_centro_medico', db_comment='Referencia a CENTROS_MEDICOS')
    estado = models.CharField(max_length=10, blank=True, null=True, db_comment='Estado: programada, atendido, etc')
    fecha_hora_turno = models.DateTimeField(db_comment='Fecha y hora de la asignacion del turno')
    solicitud_turno = models.CharField(max_length=8, blank=True, null=True, db_comment='Solicitado a partir de los 10m del centro medico')
    categoria_turno = models.CharField(max_length=19, blank=True, null=True, db_comment='El paciente escoge la opcion')
    modulo_asignado = models.CharField(max_length=100, blank=True, null=True, db_comment='Modulo asignado: Facturacion, Laboratorios, Atencion, etc')
    letra = models.CharField(max_length=1)
    numero = models.IntegerField()
    creado = models.DateTimeField(auto_now_add=True)       # NOT NULL obligatorio
    creado_en = models.DateTimeField(blank=True, null=True)



    class Meta:
        managed = True
        db_table = 'turnos'
        unique_together = (('fecha_hora_turno', 'id_profesional'),)




class AntecedentesPaciente(models.Model):
    id_antecedente = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    id_paciente = models.ForeignKey('Pacientes', models.DO_NOTHING, db_column='id_paciente', db_comment='Referencia a PACIENTES')
    TIPO_ANTECEDENTE_CHOICES = [
        ('Familiar', 'Familiar'),
        ('Personal', 'Personal'),
        ('Laboral', 'Laboral'),
    ]
    tipo_antecedente = models.CharField(
        max_length=13,
        choices=TIPO_ANTECEDENTE_CHOICES,
        db_comment='si es: familiar, personal, etc'
    )
    descripcion = models.TextField(db_comment='Descripcion')
    fecha_registro = models.DateField(blank=True, null=True, db_comment='Fecha de registro')
    SEVERIDAD_CHOICES = [
        ('Leve', 'Leve'),
        ('Moderada', 'Moderada'),
        ('Alta', 'Alta'),
    ]
    severidad = models.CharField(max_length=8, choices=SEVERIDAD_CHOICES, blank=True, null=True, db_comment='es: leve, moderada, etc')
    ESTADO_ANTECEDENTE_CHOICES = [
        ('Activo', 'Activo'),
        ('Resuelto', 'Resuelto'),
        ('Pendiente', 'Pendiente'),
    ]
    estado_antecedente = models.CharField(max_length=14, choices=ESTADO_ANTECEDENTE_CHOICES, blank=True, null=True, db_comment='Esta: activo, resuelto, etc')

    class Meta:
        managed = True
        db_table = 'antecedentes_paciente'

    def __str__(self):
        return f'Antecedente de {self.id_paciente}: {self.tipo_antecedente}'


class ResultadosLaboratorio(models.Model):
    id_resultado = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    id_paciente = models.ForeignKey('Pacientes', models.DO_NOTHING, db_column='id_paciente', db_comment='Referencia a PACIENTES')
    id_laboratorista = models.ForeignKey('ProfesionalSalud', models.DO_NOTHING, db_column='id_laboratorista', blank=True, null=True, db_comment='Referencia al laboratorista-USUARIOS que registro')
    id_servicio = models.ForeignKey('Servicios', models.DO_NOTHING, db_column='id_servicio', blank=True, null=True, db_comment='Referencia a SERVICIOS')
    fecha_solicitud = models.DateField(db_comment='Fecha en que se solicito el examen')
    fecha_resultado = models.DateTimeField(blank=True, null=True, db_comment='Fecha en que se registro el resultado')
    tipo_examen = models.CharField(max_length=200, db_comment='tipo de examenes solicitados')
    resultado = models.TextField(db_comment='Resultados de los examenes de laboratorio')
    observaciones = models.TextField(blank=True, null=True, db_comment='Notas adicionales')
    estado = models.CharField(max_length=10, blank=True, null=True, db_comment='Esta: pendiente, registrado, etc')
    codigo_qr = models.CharField(max_length=255, blank=True, null=True, db_comment='Codigo QR para descarga')
    fecha_registro = models.DateTimeField(blank=True, null=True, db_comment='Fecha de registro')

    class Meta:
        managed = True
        db_table = 'resultados_laboratorio'

    def __str__(self):
        return f'Resultado de {self.tipo_examen} para {self.id_paciente}'


class Incapacidad(models.Model):
    id_incapacidad = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    id_consulta = models.ForeignKey('Consulta', models.DO_NOTHING, db_column='id_consulta', db_comment='Consulta que genero la incapacidad')
    id_paciente = models.ForeignKey('Pacientes', models.DO_NOTHING, db_column='id_paciente', db_comment='Paciente al que se le emite la incapacidad')
    id_profesional = models.ForeignKey('ProfesionalSalud', models.DO_NOTHING, db_column='id_profesional', db_comment='Profesional que emite la incapacidad')
    fecha_inicio = models.DateField(db_comment='Fecha de inicio de la incapacidad')
    fecha_fin = models.DateField(db_comment='Fecha de fin de la incapacidad')
    dias_incapacidad = models.IntegerField(blank=True, null=True, db_comment='Dias totales de la incapacidad')
    motivo = models.TextField(db_comment='Motivo de la incapacidad')
    diagnostico_relacionado = models.TextField(blank=True, null=True, db_comment='Diagnostico que justifica la incapacidad')
    observaciones = models.TextField(blank=True, null=True, db_comment='Notas adicionales')
    estado = models.CharField(max_length=10, blank=True, null=True, db_comment='Esta: activa, finalizada, etc')
    codigo_qr = models.CharField(max_length=255, blank=True, null=True, db_comment='Codigo QR para descarga de la incapacidad')
    fecha_emision = models.DateTimeField(blank=True, null=True, db_comment='Fecha de emision incapacidad')

    class Meta:
        managed = True
        db_table = 'incapacidad'

    def __str__(self):
        return f'Incapacidad para {self.id_paciente} del {self.fecha_inicio} al {self.fecha_fin}'

