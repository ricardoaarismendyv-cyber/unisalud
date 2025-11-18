from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import usuarios, roles, rol_usuario

@admin.register(usuarios)
class CustomUsuariosAdmin(UserAdmin):
    # Puedes personalizar list_display, fieldsets, etc.
    list_display = ['nombre_usuario', 'cedula', 'tarjeta_identidad','cedula_extranjeria', 'registro_civil', 'id_rol']
    list_filter = ['id_role', 'roles']
    search_fields = ['nombre_usuario', 'roles']

@admin.register(roles)
class rolesAdmin(admin.ModelAdmin):
    list_display = ['nombre_rol', 'usuario', 'prof_salud','administracion']
    list_filter = ['usuario', 'prof_salud','administracion']
    search_fields = ['nombre_rol']

@admin.register(rol_usuario)
class rol_usuarioAdmin(admin.ModelAdmin):
    list_display = ['id_usuario', 'roles']
    list_filter = ['roles']
    search_fields = ['id_usuario_usuarios', 'roles_nombre_rol']