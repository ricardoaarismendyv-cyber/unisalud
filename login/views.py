#from django.shortcuts import render, get_object_or_404
#from django.contrib.auth import authenticate, login as django_login, logout as django_logout, get_user_model
#from prof_salud.models import Usuarios as Roles

#User = get_user_model()


# Create your views here.


#def login(request):
    #return render(request, 'paginas/login.html' )


#def login_view(request):
 #   """
  #  Login tradicional contra tabla usuarios de PostgreSQL.
   # Obtiene el rol y redirige según el rol.
    #"""
    #if request.method == 'POST':
    #    username = request.POST.get('username')
    #    password = request.POST.get('password')
        
        # Usar authenticate() que llama al backend UnisaludBackend
    #    user = authenticate(request, username=username, password=password)
        
    #    if user is not None:
    #        django_login(request, user)
            
            # Obtener rol del backend
    #        role_name = getattr(user, 'profile_role', None)
            
            # Fallback: consultar BD si el backend no lo adjuntó
    #        if not role_name:
    #            try:
    #                perfil = PerfilUsuario.objects.select_related('id_rol').get(
    #                    nombre_usuario=username
    #                )
    #                if perfil and perfil.id_rol:
    #                    role_name = getattr(perfil.id_rol, 'nombre_rol', None)
    #            except Exception:
    #                role_name = None
            
            # Guardar rol en sesión
    #        request.session['role'] = role_name or 'unknown'
            
            # Mapa de redirecciones por rol
    #        redirect_map = {
    #            'paciente': '/usuario/',
    #            'profesional_salud': '/profesionalS/',
    #            'laboratorista': '/laboratorio/',
    #            'recepcionista': '/administrativo/',
    #            'admin_centro_medico': '/administrativo/',
    #            'admin': '/admin/',
    #        }
            
            # Normalizar rol
    #        key = (role_name or '').strip().lower().replace(' ', '_')
    #        target = redirect_map.get(key, '/')
            
    #        return redirect(target)
    #    else:
    #        from django.contrib import messages
    #        messages.error(request, 'Credenciales inválidas')
    #        return render(request, 'login/login.html', {'error': 'Credenciales inválidas'})
    
    #return render(request, 'login/login.html')


#def logout_view(request):
#    django_logout(request)
#    request.session.flush()
#    return redirect('login')
