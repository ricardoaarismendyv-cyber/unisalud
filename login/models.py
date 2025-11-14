from django.db import models
#from django.contrib.auth.models import AbstractUser

# Create your models here.
class roles(models.Model): 
    id_rol = models.AutoField(primary_key=True, db_comment='ID autoincremental del roles')
    nombre_rol = models.CharField(unique=True, max_length=50, db_comment='Nombre de los roles: paciente, profesional_salud, laboratorista, recepcionista, admin_centro_medico')
    descripcion = models.TextField(blank=True, null=True, db_comment='Descripcion de los roles para mayor claridad, opcional')

    #PERMISSION_CHOICES =[
    #    (0, 'No Access'), NO ACCESS
    #    (1, 'view only'), VIEW
    #    (2, 'create and modify'), CREATE AND MODIFY
    #]

    #nombre_rol = models.models.CharField(max_length=50, primary_key=True, db_comment='Nombre del rol de usuario')
    #usuario = models.models.IntegerField(choices = PERMISSION_CHOICES.default-0)
    #profesional_salud = models.models.IntegerField(choices = PERMISSION_CHOICES.default-0)
    #administrativo = models.models.IntegerField(choices = PERMISSION_CHOICES.default-0)


    class Meta:
        managed = True
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.nombre_rol


class usuarios(models.Model): #(AbstractUser):
    id_usuario = models.AutoField(primary_key=True, db_comment='ID autoincremental del usuario')
    id_rol = models.ForeignKey('roles', models.DO_NOTHING, db_column='id_rol', db_comment='Rol asignado para pacientes, profesional salud, recepcionista, laboratorista, adm centro')
    nombre_usuario = models.CharField(unique=True, max_length=50, db_comment='Login unico para el usuario')
    contrasena = models.CharField(max_length=255, db_comment='Contrasena que crea el usuario')
    email = models.CharField(unique=True, max_length=100, blank=True, null=True, db_comment='Correo principal-login del usuario')
    ultimo_login = models.DateTimeField(blank=True, null=True, db_comment='ultimo inicio de sesion')
    estado = models.CharField(max_length=9, blank=True, null=True, db_comment='Esta: activo, inactivo,etc')

    #USERNAME_FIELD = 'nombre_rol'

    class Meta:
        managed = True
        db_table = 'usuarios'

    def __str__(self):
        return self.nombre_usuario

#class rol_usuario(models.Model):
#    id_usuario = models.models.ForeignKey(usuarios, on_delete-models.CASCADE)
#    roles = models.ForeignKey(roles, on_delete=models.CASCADE)

#    class Meta:
#        managed = True
#        db_table = 'rol_usuario'
#        verbose_name = 'Rol Usuario'
#        verbose_name_plural = 'Roles Usuarios'
#        unique_together = (('id_usuario', 'roles'),)
#    def __str__(self):
#        return f"{self.usuarios_id_username} - {self.roles_nombre_rol}"