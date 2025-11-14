from django.shortcuts import render, redirect
from django.contrib.auth import autenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm
from .models import usuarios, roles

#User = get_user_model()


# Create your views here.


#def login(request):
    #return render(request, 'paginas/login.html' )


def login_view(request):
        if request.user.is_authenticated:
                return redirect('inicio-usuario')
        """Login tradicional contra tabla usuarios de PostgreSQL.
        Obtiene el rol y redirige según el rol."""

        if request.method == 'POST':
        
                form = LoginForm(request, data=request.POST)
                if form.is_valid():
                        nombre_usuario = form.cleaned_data.get('nombre_usuario')
                        contrasena = form.cleaned_data.get('contrasena')
                        usuarios = authenticate(username=nombre_usuario, password=contrasena)
                        if usuarios is not None:
                                login(request, usuarios)
                                return redirect('inicio-usuario')
                        else:
                                messages.error(request, 'usuario o contraseña inválidos')
                else:
                        form = LoginForm()
                return render(request, 'login/login.html', {'form': form})
                
@login_required
def logout_view(request):
        logout(request)
        messages.success(request, 'Has cerrado sesión exitosamente.')
        return redirect('login')
