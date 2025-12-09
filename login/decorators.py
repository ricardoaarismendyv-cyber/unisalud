from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Verificamos si el 'id_usuario' está en la sesión, en lugar de usar request.user.is_authenticated.
            if 'id_usuario' not in request.session:
                messages.error(request, 'Debes iniciar sesión para ver esta página.')
                return redirect('login')
            
            user_roles = request.session.get('roles', [])
            
            # Comprobamos si hay alguna coincidencia entre los roles del usuario y los roles permitidos.
            # La función any() devuelve True si al menos un rol del usuario está en allowed_roles.
            if not any(role in allowed_roles for role in user_roles):
                messages.error(request, 'No tienes permiso para acceder a esta página.')
                return redirect('login') # O a una página de "acceso denegado"
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
