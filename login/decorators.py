from django.shortcuts import redirect
from django.contrib import messages

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if 'nombre_rol' not in request.session:
                messages.error(request, 'Debes iniciar sesión para ver esta página.')
                return redirect('login')
            
            if request.session['nombre_rol'] not in allowed_roles:
                messages.error(request, 'No tienes permiso para acceder a esta página.')
                return redirect('login') # O a una página de "acceso denegado"
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

#Este decorador se encargará de verificar que un usuario haya iniciado sesión y que tenga el rol correcto antes de permitirle el acceso a una vista.