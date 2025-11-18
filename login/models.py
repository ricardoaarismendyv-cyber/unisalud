from django.contrib.auth.models import AbstractUser
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

class usuarios(AbstractUser):
    id_usuario = models.AutoField(primary_key=True, db_comment='ID autoincremental del usuario')
    id_rol = models.ForeignKey('roles', models.DO_NOTHING, db_column='id_rol', db_comment='Rol asignado para pacientes, profesional salud, recepcionista, laboratorista, adm centro')
    id_tipo_identificacion = models.ForeignKey('tipoidentificacion', models.DO_NOTHING, db_column='id_tipo_identificacion', db_comment='Referencia a TIPO_IDENTIFICACION')
    cedula = models.IntegerField(unique=True, blank=True, null=True)
    tarjeta_identidad = models.IntegerField(unique=True, blank=True, null=True)
    registro_civil = models.IntegerField(unique=True, blank=True, null=True)
    cedula_extranjeria = models.IntegerField(unique=True, blank=True, null=True)
    nombre_usuario = models.CharField(unique=True, max_length=50, db_comment='Login unico para el usuario')
    contrasena = models.CharField(max_length=255, db_comment='Contrasena que crea el usuario')
    
    USERNAME_FIELD = 'nombre_usuario'  # Campo utilizado para autenticación
    REQUIRED_FIELDS = ['id_rol', 'id_tipo_identificacion']  # Campos obligatorios además de USERNAME_FIELD
    
    class Meta:
        managed = True
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    #def __str__(self):
    #    return f'{self.username} - {self.get_full_name()}'

#OJO Esta tabla no fue creada inicialmente en la BD (SE DEBE INCLUR), esta permite conectar los roles con los usuarios
class rol_usuario(models.Model):
    id_usuario = models.ForeignKey(usuarios, on_delete=models.CASCADE)
    roles = models.ForeignKey(roles, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'rolUsuario'
        verbose_name = 'rUsuario'
        verbose_name_plural = 'rolesUsuarios'
        unique_together = ('id_usuario', 'roles'),
        
    def __str__(self):
        return f"{self.id_usuario_usuarios} - {self.roles.nombre_rol}"

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