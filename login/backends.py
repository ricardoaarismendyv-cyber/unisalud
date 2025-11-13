#from django.contrib.auth import get_user_model
#from django.contrib.auth.hashers import check_password
#from prof_salud.models import Usuarios as PerfilUsuario

#UserModel = get_user_model()

#class UnisaludBackend:
#    """
#    Backend de autenticación contra tabla PostgreSQL `usuarios`.
#    - Busca usuario por nombre_usuario.
#    - Valida contraseña (hasheada o texto plano).
#    - Obtiene/crea User de Django.
#    - Adjunta atributo `profile_role` con el nombre del rol.
#    """
    
#    def authenticate(self, request, username=None, password=None, **kwargs):
#        if username is None or password is None:
#            return None
        
#        try:
#            perfil = PerfilUsuario.objects.select_related('id_rol').get(
#                nombre_usuario=username
#            )
#        except PerfilUsuario.DoesNotExist:
#            return None

#        stored_password = perfil.contrasena or ''
#        password_valid = False
        
#        try:
#            password_valid = check_password(password, stored_password)
#        except Exception:
#            password_valid = (password == stored_password)

#        if not password_valid:
#            return None

#        try:
#            user, created = UserModel.objects.get_or_create(
#                username=username,
#                defaults={'is_active': True}
#            )
#        except Exception:
#            return None

#        role_name = None
#        if perfil.id_rol:
#            role_name = getattr(perfil.id_rol, 'nombre_rol', None)
        
#        setattr(user, 'profile_role', role_name)

#        return user

#    def get_user(self, user_id):
#        try:
#            return UserModel.objects.get(pk=user_id)
#        except UserModel.DoesNotExist:
#            return None
