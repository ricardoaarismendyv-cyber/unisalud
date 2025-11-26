from django.contrib import admin
from usuario.models import Usuarios, Roles, Pacientes, ProfesionalSalud

@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    # Usar método personalizado en lugar del campo ManyToMany directamente
    list_display = ['id_usuario', 'nombre_usuario', 'email', 'mostrar_roles']
    list_filter = ['roles']
    search_fields = ['nombre_usuario', 'email']
    ordering = ['id_usuario']
    filter_horizontal = ['roles']  # Widget mejorado para ManyToMany
    
    fieldsets = (
        ('Información de Cuenta', {
            'fields': ('nombre_usuario', 'email', 'contrasena', 'roles')
        }),
    )
    
    # Método personalizado para mostrar roles en list_display
    def mostrar_roles(self, obj):
        return ", ".join([rol.nombre_rol for rol in obj.roles.all()])
    mostrar_roles.short_description = 'Roles'  # Nombre de columna en el admin
    
    def save_model(self, request, obj, form, change):
        # Si la contraseña cambió, hashearla
        if 'contrasena' in form.changed_data:
            obj.set_password(obj.contrasena)
        super().save_model(request, obj, form, change)