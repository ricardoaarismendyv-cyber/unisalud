from django.db import models

class roles(models.Model): 
    PERMISSION_CHOICES =[
        (0, 'No Access'), 
        (1, 'view only'), 
        (2, 'create and modify'),
    ]
    id_rol = models.AutoField(primary_key=True, db_comment='ID autoincremental del roles')
    nombre_rol = models.CharField(unique=True, max_length=50, db_comment='Nombre de los roles: paciente, profesional_salud, laboratorista, recepcionista, admin_centro_medico')
    descripcion = models.TextField(blank=True, null=True, db_comment='Descripcion de los roles para mayor claridad, opcional')
    
    usuario = models.IntegerField(choices = PERMISSION_CHOICES, default=0) #definir roles 0= a no acceso, 1 ver 2 crear y modificar
    profesional_salud = models.IntegerField(choices = PERMISSION_CHOICES, default=0)
    administrativo = models.IntegerField(choices = PERMISSION_CHOICES, default=0)

    class Meta:
        managed = True
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.nombre_rol

class usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True, db_comment='ID autoincremental del usuario')
    id_rol = models.ForeignKey('roles', models.DO_NOTHING, db_column='id_rol', db_comment='Rol asignado para pacientes, profesional salud, recepcionista, laboratorista, adm centro')
    nombre_usuario = models.CharField(unique=True, max_length=50, db_comment='Login unico para el usuario')
    contrasena = models.CharField(max_length=255, db_comment='Contrasena que crea el usuario')
    email = models.CharField(unique=True, max_length=100, blank=True, null=True, db_comment='Correo principal-login del usuario')
    ultimo_login = models.DateTimeField(blank=True, null=True, db_comment='ultimo inicio de sesion')
    estado = models.CharField(max_length=9, blank=True, null=True, db_comment='Esta: activo, inactivo,etc')

    class Meta:
        managed = True
        db_table = 'usuario'

    def __str__(self):
        return f'{self.username} - {self.get_full_name()}'

class tipoidentificacion(models.Model):
    id_tipo_identificacion = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    identificacion = models.CharField(unique=True, max_length=50, db_comment='Tipo de identificacion: cedula, tarjeta, etc')
    nombre_identificacion = models.CharField(max_length=50, db_comment='Nombre de la abreviatura, CC: cedula de ciudadania')
    descripcion = models.TextField(blank=True, null=True, db_comment='Descripcion opcional')

    class Meta:
        managed = True
        db_table = 'tipo_identificacion'
        verbose_name = 'Tipo de Identificacion'
        verbose_name_plural = 'Tipos de Identificacion'

    def __str__(self):
        return self.nombre_identificacion


class genero(models.Model):
    id_genero = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_genero = models.CharField(unique=True, max_length=20, db_comment='Ej: Masculino, Femenino, No Binario, etc')

    
    def __str__(self):
        return self.nombre_genero
    
    class Meta:
        managed = True
        db_table = 'genero'


class gruporh(models.Model):
    id_rh = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    tipo_rh = models.CharField(unique=True, max_length=3, db_comment='Ej: A+, B-, etc')

    
    def __str__(self):
        return self.tipo_rh
    
    class Meta:
        managed = True
        db_table = 'grupo_rh'


class estadocivil(models.Model):
    id_estado_civil = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_estado = models.CharField(unique=True, max_length=20, db_comment='Ej: soltero, casado, etc')

    class Meta:
        managed = True
        db_table = 'estado_civil'

    def __str__(self):
        return self.nombre_estado


class estratosocioeconomico(models.Model):
    id_estrato = models.IntegerField(primary_key=True, db_comment='ID del 1 al 6')
    descripcion = models.CharField(max_length=100, db_comment='Ej: Bajo, Medio, alto')

    class Meta:
        managed = True
        db_table = 'estrato_socioeconomico'

    def __str__(self):
        return f'Estrato {self.id_estrato}'


class regionsalud(models.Model):
    id_region = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_region = models.CharField(unique=True, max_length=100, db_comment='Nombre de la region Ej: caribe, eje cafetero, sur occidente, etc')
    descripcion = models.TextField(blank=True, null=True, db_comment='Descripcion')

    class Meta:
        managed = True
        db_table = 'regionsalud'

    def __str__(self):
        return self.nombre_region


class departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_departamento = models.CharField(max_length=100, db_comment='Nombre del departamento')
    id_region = models.ForeignKey('regionsalud', models.DO_NOTHING, db_column='id_region', blank=True, null=True, db_comment='Referencia a REGION_SALUD')
    codigo_dane = models.CharField(max_length=10, blank=True, null=True, db_comment='Codigo DANE para identificar oficialmente c-depto.')

    class Meta:
        managed = True
        db_table = 'departamento'

    def __str__(self):
        return self.nombre_departamento


class ciudad(models.Model):
    id_ciudad = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_ciudad = models.CharField(max_length=100, db_comment='Nombre de la ciudad')
    id_departamento = models.ForeignKey('departamento', models.DO_NOTHING, db_column='id_departamento', db_comment='Referencia a DEPARTAMENTO')
    codigo_dane = models.CharField(max_length=10, blank=True, null=True, db_comment='Codigo DANE para identificar oficialmente c-ciudad')

    class Meta:
        managed = True
        db_table = 'ciudad'

    def __str__(self):
        return self.nombre_ciudad


class redessalud(models.Model):
    id_red = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_red = models.CharField(unique=True, max_length=150, db_comment='Nombre de la red: RIPSS (Redes integrales de prestadores de servicios de salud)')
    descripcion = models.TextField(blank=True, null=True, db_comment='Descripcion')
    id_region = models.ForeignKey('regionsalud', models.DO_NOTHING, db_column='id_region', blank=True, null=True, db_comment='Referencia a REGION_SALUD')
    estado_red = models.CharField(max_length=8, blank=True, null=True, db_comment='Esta activa, inactiva')

    class Meta:
        managed = True
        db_table = 'redessalud'

    def __str__(self):
        return self.nombre_red


class nivelesatencion(models.Model):
    id_nivel = models.IntegerField(primary_key=True, db_comment='ID del nivel (1 a 3)')
    nombre_nivel = models.CharField(max_length=50, db_comment='de acuerdo al grado de complejidad en salud: primer nivel-atencion basica')
    descripcion = models.TextField(blank=True, null=True, db_comment='Descripcion')

    class Meta:
        managed = True
        db_table = 'nivelesatencion'

    def __str__(self):
        return self.nombre_nivel


class centrosmedicos(models.Model):
    id_centro_medico = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_centro = models.CharField(max_length=150, db_comment='Nombre del centro medico')
    id_red_salud = models.ForeignKey('redessalud', models.DO_NOTHING, db_column='id_red_salud', blank=True, null=True, db_comment='Referencia a redessalud')
    id_nivel_atencion = models.ForeignKey('nivelesatencion', models.DO_NOTHING, db_column='id_nivel_atencion', db_comment='Referencia a NIVELES_ATENCION')
    id_ciudad = models.ForeignKey('ciudad', models.DO_NOTHING, db_column='id_ciudad', db_comment='Referencia a CIUDAD')
    direccion = models.CharField(max_length=255, db_comment='Direccion centro medico')
    latitud = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True, db_comment='Latitud, localizacion geografica')
    longitud = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True, db_comment='Longitud, localizacion geografica')
    telefono = models.CharField(max_length=15, blank=True, null=True, db_comment='Telefono centro medico')
    celular = models.CharField(max_length=15, blank=True, null=True, db_comment='Celular centro medico')
    correo = models.CharField(max_length=100, blank=True, null=True, db_comment='Correo entro medico')
    sitio_web = models.CharField(max_length=150, blank=True, null=True, db_comment='Sitio web centro medico')
    codigo_habilitacion = models.CharField(unique=True, max_length=50, blank=True, null=True, db_comment='Codigo de habilitacion REPS')
    fecha_habilitacion = models.DateField(blank=True, null=True, db_comment='Fecha de habilitacion REPS')
    estado_centro = models.CharField(max_length=10, blank=True, null=True, db_comment='Esta activa, inactiva')

    class Meta:
        managed = True
        db_table = 'centrosmedicos'

    def __str__(self):
        return self.nombre_centro


class eps(models.Model):
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


class tiposafiliacion(models.Model):
    id_tipo_afiliacion = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_tipo = models.CharField(unique=True, max_length=20, db_comment='el paciente esta en regimen Contributivo, Subsidiado, etc')

    class Meta:
        managed = True
        db_table = 'tiposafiliacion'

    def __str__(self):
        return self.nombre_tipo


class especialidades(models.Model):
    id_especialidad = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_especialidad = models.CharField(unique=True, max_length=100, db_comment='refiere a la especialidad medica: neurologia, cardiologia, etc')
    descripcion = models.TextField(blank=True, null=True, db_comment='Descripcion')
    nivel_formacion = models.CharField(max_length=15, blank=True, null=True, db_comment='Nivel de formacion')

    class Meta:
        managed = True
        db_table = 'especialidades'

    def __str__(self):
        return self.nombre_especialidad


class medicamentos(models.Model):
    id_medicamento = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_comercial = models.CharField(max_length=200, db_comment='Nombre comercial medicamento')
    nombre_generico = models.CharField(max_length=200, blank=True, null=True, db_comment='Nombre generico medicamento')
    principio_activo = models.CharField(max_length=100, blank=True, null=True, db_comment='Principio activo medicamento')
    concentracion = models.CharField(max_length=50, blank=True, null=True, db_comment='Concentracion medicamento')
    forma_farmaceutica = models.CharField(max_length=50, blank=True, null=True, db_comment='Forma farmaceutica medicamento')
    via_administracion = models.CharField(max_length=50, blank=True, null=True, db_comment='Via de administracion medicamento')
    registro_invima = models.CharField(unique=True, max_length=100, db_comment='Registro INVIMA del medicamento')
    fabricante = models.CharField(max_length=150, blank=True, null=True, db_comment='Fabricante del medicamento')
    estado_medicamento = models.CharField(max_length=11, blank=True, null=True, db_comment='Esta activo, retirado, etc')
    fecha_registro = models.DateTimeField(blank=True, null=True, db_comment='Fecha de registro medicamento')

    class Meta:
        managed = True
        db_table = 'medicamentos'

    def __str__(self):
        return self.nombre_comercial


class servicios(models.Model):
    id_servicio = models.AutoField(primary_key=True, db_comment='ID autoincremental del servicio')
    nombre_servicio = models.CharField(max_length=200, db_comment='Nombre del servicio medico')
    descripcion = models.TextField(blank=True, null=True, db_comment='Descripcion detallada del servicio medico')
    tipo_servicio = models.CharField(max_length=21, db_comment='Categoria: imagenologia, laboratorio, etc')
    id_especialidad = models.ForeignKey('especialidades', models.DO_NOTHING, db_column='id_especialidad', blank=True, null=True, db_comment='Especialidad requerida (opcional)')
    estado = models.CharField(max_length=10, blank=True, null=True, db_comment='Esta activo, inactivo, etc')
    fecha_registro = models.DateTimeField(blank=True, null=True, db_comment='Fecha de creacion')

    class Meta:
        managed = True
        db_table = 'servicios'

    def __str__(self):
        return self.nombre_servicio


class enfermedades(models.Model):
    id_enfermedad = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    codigo_cie10 = models.CharField(unique=True, max_length=10, db_comment='Codigo CIE-10 para clasificar diagnosticos, sintomas')
    nombre_enfermedad = models.CharField(max_length=300, db_comment='Nombre de la enfermedad')
    descripcion = models.TextField(blank=True, null=True, db_comment='Descripcion clinica de la enfermedad')
    categoria = models.CharField(max_length=100, blank=True, null=True, db_comment='refiere si es aguda, cronica, infecciosa, etc')

    class Meta:
        managed = True
        db_table = 'enfermedades'

    def __str__(self):
        return self.nombre_enfermedad


class estadoorden(models.Model):
    id_estado_orden = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_estado_orden = models.CharField(unique=True, max_length=20, db_comment='esta: pendiente, entregada, etc')

    class Meta:
        managed = True
        db_table = 'estadoorden'

    def __str__(self):
        return self.nombre_estado_orden


class tipoorden(models.Model):
    id_tipo = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    nombre_tipo = models.CharField(unique=True, max_length=50, db_comment='Es: Medicamentos, examenes, etc')

    class Meta:
        managed = True
        db_table = 'tipoorden'

    def __str__(self):
        return self.nombre_tipo

class pacientes(models.Model):
    id_paciente = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    id_usuario = models.OneToOneField('usuarios', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True, db_comment='Referencia a la cuenta de USUARIOS')
    id_tipo_identificacion = models.ForeignKey('tipoidentificacion', models.DO_NOTHING, db_column='id_tipo_identificacion', db_comment='Referencia a TIPO_IDENTIFICACION')
    numero_documento = models.CharField(max_length=20, db_comment='Numero del documento paciente')
    nombre1 = models.CharField(max_length=50, db_comment='Primer nombre paciente')
    nombre2 = models.CharField(max_length=50, blank=True, null=True, db_comment='Segundo nombre paciente, opcional')
    apellido1 = models.CharField(max_length=50, db_comment='Primer apellido paciente')
    apellido2 = models.CharField(max_length=50, blank=True, null=True, db_comment='Segundo apellido paciente, opcional')
    id_genero = models.ForeignKey('genero', models.DO_NOTHING, db_column='id_genero', db_comment='Referencia a GENERO')
    id_rh = models.ForeignKey('gruporh', models.DO_NOTHING, db_column='id_rh', blank=True, null=True, db_comment='Referencia a GRUPO_RH')
    fecha_nacimiento = models.DateField(db_comment='Fecha de nacimiento paciente')
    id_estado_civil = models.ForeignKey('estadocivil', models.DO_NOTHING, db_column='id_estado_civil', blank=True, null=True, db_comment='Referencia a ESTADO_CIVIL')
    id_estrato = models.ForeignKey('estratosocioeconomico', models.DO_NOTHING, db_column='id_estrato', blank=True, null=True, db_comment='Referencia a ESTRATO')
    direccion = models.CharField(max_length=255, blank=True, null=True, db_comment='Direccion paciente')
    celular = models.CharField(max_length=15, blank=True, null=True, db_comment='Celular paciente')
    telefono = models.CharField(max_length=15, blank=True, null=True, db_comment='Telefono fijo paciente, opcional')
    correo_electronico = models.CharField(max_length=100, blank=True, null=True, db_comment='Correo paciente, opcional')
    fecha_registro = models.DateTimeField(blank=True, null=True, db_comment='Fecha de registro paciente')

    class Meta:
        managed = True
        db_table = 'pacientes'
        unique_together = (('id_tipo_identificacion', 'numero_documento'),)

    def __str__(self):
        return f'{self.nombre1} {self.apellido1}'


class profesionalsalud(models.Model):
    id_profesional = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    id_usuario = models.OneToOneField('usuarios', models.DO_NOTHING, db_column='id_usuario', db_comment='Referencia a la cuenta de USUARIOS (Obligatorio para personal)')
    id_tipo_identificacion = models.ForeignKey('tipoidentificacion', models.DO_NOTHING, db_column='id_tipo_identificacion', db_comment='Referencia a TIPO_IDENTIFICACION')
    numero_documento = models.CharField(max_length=20, db_comment='Numero del documento profesional salud')
    nombre1 = models.CharField(max_length=50, db_comment='Primer nombre profesional salud')
    nombre2 = models.CharField(max_length=50, blank=True, null=True, db_comment='Segundo nombre profesional salud')
    apellido1 = models.CharField(max_length=50, db_comment='Primer apellido profesional salud')
    apellido2 = models.CharField(max_length=50, blank=True, null=True, db_comment='Segundo apellido profesional salud')
    id_genero = models.ForeignKey('genero', models.DO_NOTHING, db_column='id_genero', db_comment='Referencia a GENERO')
    fecha_nacimiento = models.DateField(blank=True, null=True, db_comment='Fecha de nacimiento profesional salud')
    telefono = models.CharField(max_length=15, blank=True, null=True, db_comment='Telefono profesional salud, opcional')
    celular = models.CharField(max_length=15, blank=True, null=True, db_comment='Celular profesional salud')
    correo = models.CharField(max_length=100, blank=True, null=True, db_comment='Correo profesional salud')
    registro_profesional = models.CharField(unique=True, max_length=50, blank=True, null=True, db_comment='Registro medico, puede ser NULL para recepcionistas-admins')
    id_especialidad = models.ForeignKey('especialidades', models.DO_NOTHING, db_column='id_especialidad', blank=True, null=True, db_comment='Referencia a ESPECIALIDADES')
    id_centro_medico = models.ForeignKey('centrosmedicos', models.DO_NOTHING, db_column='id_centro_medico', db_comment='Centro medico donde trabaja (Obligatorio)')
    fecha_vinculacion = models.DateField(blank=True, null=True, db_comment='Fecha de vinculacion')
    estado = models.CharField(max_length=10, blank=True, null=True, db_comment='Esta: activo, inactivo, etc')

    class Meta:
        managed = True
        db_table = 'profesionalsalud'
        unique_together = (('id_tipo_identificacion', 'numero_documento'),)
        verbose_name = 'Profesional de Salud'
        verbose_name_plural = 'Profesionales de Salud'

    def __str__(self):
        return f'{self.nombre1} {self.apellido1}'


class afiliacion(models.Model):
    id_afiliacion = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    id_paciente = models.ForeignKey('pacientes', models.DO_NOTHING, db_column='id_paciente', db_comment='Referencia a PACIENTES')
    id_eps = models.ForeignKey('eps', models.DO_NOTHING, db_column='id_eps', db_comment='Referencia a EPS')
    id_tipo_afiliacion = models.ForeignKey('tiposafiliacion', models.DO_NOTHING, db_column='id_tipo_afiliacion', db_comment='Referencia a TIPOS_AFILIACION')
    fecha_inicio = models.DateField(db_comment='Fecha de inicio afliacion')
    fecha_fin = models.DateField(blank=True, null=True, db_comment='Fecha de fin de la afiliacion')
    estado_afiliacion = models.CharField(max_length=10, blank=True, null=True, db_comment='Esta: activo, inactiva')

    class Meta:
        managed = True
        db_table = 'afiliacion'

    def __str__(self):
        return f'Afiliación de {self.id_paciente} a {self.id_eps}'


class detallemedicamento(models.Model):
    id_detalle = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    id_medicamento = models.ForeignKey('medicamentos', models.DO_NOTHING, db_column='id_medicamento', db_comment='Referencia al medicamento principal')
    lote = models.CharField(max_length=50, db_comment='Numero de lote medicamento')
    fecha_expiracion = models.DateField(db_comment='Fecha de vencimiento medicamento')
    condiciones_almacenamiento = models.TextField(blank=True, null=True, db_comment='Condiciones de almacenamiento medicamento')
    cantidad_existente = models.IntegerField(blank=True, null=True, db_comment='Cantidad disponible medicamento')
    fecha_ingreso = models.DateTimeField(blank=True, null=True, db_comment='Fecha de ingreso medicamento')
    estado = models.CharField(max_length=8, blank=True, null=True, db_comment='Estado del lote: activo, agotado, etc')

    class Meta:
        managed = True
        db_table = 'detallemedicamento'
        unique_together = (('id_medicamento', 'lote'),)

    def __str__(self):
        return f'{self.id_medicamento} - Lote: {self.lote}'


class consulta(models.Model):
    id_consulta = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    id_paciente = models.ForeignKey('pacientes', models.DO_NOTHING, db_column='id_paciente', db_comment='Referencia a PACIENTES')
    id_profesional = models.ForeignKey('profesionalsalud', models.DO_NOTHING, db_column='id_profesional', db_comment='Referencia a PROFESIONAL_SALUD')
    id_centro_medico = models.ForeignKey('centrosmedicos', models.DO_NOTHING, db_column='id_centro_medico', db_comment='Referencia a CENTROS_MEDICOS')
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


class ordenmedica(models.Model):
    id_orden = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    id_paciente = models.ForeignKey('pacientes', models.DO_NOTHING, db_column='id_paciente', db_comment='Referencia a PACIENTE')
    id_profesional = models.ForeignKey('profesionalsalud', models.DO_NOTHING, db_column='id_profesional', db_comment='Referencia a PROFESIONAL_SALUD')
    id_tipo_orden = models.ForeignKey('tipoorden', models.DO_NOTHING, db_column='id_tipo_orden', db_comment='Referencia a TIPO_ORDEN')
    id_detalle_medicamento = models.ForeignKey('detallemedicamento', models.DO_NOTHING, db_column='id_detalle_medicamento', blank=True, null=True, db_comment='Referencia a DETALLE_MEDICAMENTOS')
    id_servicio = models.ForeignKey('servicios', models.DO_NOTHING, db_column='id_servicio', blank=True, null=True, db_comment='Referencia a SERVICIOS')
    dosis = models.CharField(max_length=100, blank=True, null=True, db_comment='Dosis del medicamento')
    duracion_tratamiento = models.CharField(max_length=100, blank=True, null=True, db_comment='De acuerdo al diagnostico')
    frecuencia = models.CharField(max_length=50, blank=True, null=True, db_comment='Frecuencia de acuerdo al diagnostico')
    cantidad = models.IntegerField(blank=True, null=True, db_comment='Cantidad de acuerdo al diagnostico')
    indicaciones = models.TextField(blank=True, null=True, db_comment='Indicaciones tratamiento y-o procedimiento')
    id_centro_medico = models.ForeignKey('centrosmedicos', models.DO_NOTHING, db_column='id_centro_medico', db_comment='Centro medico donde se emite')
    id_estado_orden = models.ForeignKey('estadoorden', models.DO_NOTHING, db_column='id_estado_orden', db_comment='Referencia a ESTADO_ORDEN')
    fecha_emision = models.DateTimeField(blank=True, null=True, db_comment='Fecha de emision de la orden')
    fecha_cumplimiento = models.DateTimeField(blank=True, null=True, db_comment='Fecha de cumplimiento, maximo 30 dias')
    codigo_qr = models.CharField(max_length=255, blank=True, null=True, db_comment='Codigo QR para descarga segura')
    id_consulta = models.ForeignKey('consulta', models.DO_NOTHING, db_column='id_consulta', blank=True, null=True, db_comment='Referencia opcional a CONSULTA')

    class Meta:
        managed = True
        db_table = 'ordenmedica'
        verbose_name = 'Orden Medica'
        verbose_name_plural = 'Ordenes Medicas'

    def __str__(self):
        return f'Orden {self.id_orden} - {self.id_paciente}'


class diagnosticopaciente(models.Model):
    id_diagnostico = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    id_consulta = models.ForeignKey('consulta', models.DO_NOTHING, db_column='id_consulta', db_comment='Referencia a CONSULTA')
    id_enfermedad = models.ForeignKey('enfermedades', models.DO_NOTHING, db_column='id_enfermedad', db_comment='Referencia a ENFERMEDADES')
    tipo_diagnostico = models.CharField(max_length=10, blank=True, null=True, db_comment='Es: presuntivo, principal, etc')
    notas = models.TextField(blank=True, null=True, db_comment='Notas')
    fecha_registro = models.DateTimeField(blank=True, null=True, db_comment='Fecha de registro')

    class Meta:
        managed = True
        db_table = 'diagnosticopaciente'

    def __str__(self):
        return f'Diagnóstico para consulta {self.id_consulta}: {self.id_enfermedad}'


class turnos(models.Model):
    id_turno = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    id_paciente = models.ForeignKey('pacientes', models.DO_NOTHING, db_column='id_paciente', db_comment='Referencia a PACIENTES')
    id_profesional = models.ForeignKey('profesionalsalud', models.DO_NOTHING, db_column='id_profesional', db_comment='Referencia a PROFESIONAL_SALUD')
    id_centro_medico = models.ForeignKey('centrosmedicos', models.DO_NOTHING, db_column='id_centro_medico', db_comment='Referencia a CENTROS_MEDICOS')
    estado = models.CharField(max_length=10, blank=True, null=True, db_comment='Esta: programada, atendido, etc')
    fecha_hora_turno = models.DateTimeField(db_comment='Fecha y hora de la asignacion del turno')
    solicitud_turno = models.CharField(max_length=8, blank=True, null=True, db_comment='Solicitado a partir de los 10m del centro medico')
    categoria_turno = models.CharField(max_length=19, blank=True, null=True, db_comment='El paciente escoge la opcion')
    modulo_asignado = models.CharField(max_length=100, blank=True, null=True, db_comment='Modulo asignado: Facturacion, Laboratorios, Atencion, etc')
    creado_en = models.DateTimeField(blank=True, null=True, db_comment='Fecha de registro')

    class Meta:
        managed = True
        db_table = 'turnos'
        unique_together = (('fecha_hora_turno', 'id_profesional'),)

    def __str__(self):
        return f'Turno para {self.id_paciente} el {self.fecha_hora_turno}'


class antecedentespaciente(models.Model):
    id_antecedente = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    id_paciente = models.ForeignKey('pacientes', models.DO_NOTHING, db_column='id_paciente', db_comment='Referencia a PACIENTES')
    tipo_antecedente = models.CharField(max_length=13, db_comment='si es: familiar, personal, etc')
    descripcion = models.TextField(db_comment='Descripcion')
    fecha_registro = models.DateField(blank=True, null=True, db_comment='Fecha de registro')
    severidad = models.CharField(max_length=8, blank=True, null=True, db_comment='es: leve, moderada, etc')
    estado_antecedente = models.CharField(max_length=14, blank=True, null=True, db_comment='Esta: activo, resuelto, etc')

    class Meta:
        managed = True
        db_table = 'antecedentespaciente'

    def __str__(self):
        return f'Antecedente de {self.id_paciente}: {self.tipo_antecedente}'


class resultadoslaboratorio(models.Model):
    id_resultado = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    id_paciente = models.ForeignKey('pacientes', models.DO_NOTHING, db_column='id_paciente', db_comment='Referencia a PACIENTES')
    id_laboratorista = models.ForeignKey('profesionalsalud', models.DO_NOTHING, db_column='id_laboratorista', blank=True, null=True, db_comment='Referencia al laboratorista-USUARIOS que registro')
    id_servicio = models.ForeignKey('servicios', models.DO_NOTHING, db_column='id_servicio', blank=True, null=True, db_comment='Referencia a SERVICIOS')
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
        db_table = 'resultadoslaboratorio'

    def __str__(self):
        return f'Resultado de {self.tipo_examen} para {self.id_paciente}'


class incapacidad(models.Model):
    id_incapacidad = models.AutoField(primary_key=True, db_comment='ID autoincremental')
    id_consulta = models.ForeignKey('consulta', models.DO_NOTHING, db_column='id_consulta', db_comment='Consulta que genero la incapacidad')
    id_paciente = models.ForeignKey('pacientes', models.DO_NOTHING, db_column='id_paciente', db_comment='Paciente al que se le emite la incapacidad')
    id_profesional = models.ForeignKey('profesionalsalud', models.DO_NOTHING, db_column='id_profesional', db_comment='Profesional que emite la incapacidad')
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