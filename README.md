# unisalud
unisalud proyecto sena 2025
_____________________________________________________
4 de noviembre
INICIO UNISALUD: Creada inicialmente para mostrar los roles, aqui esta el codigo utilizado:
{% extends 'plantilla_ps.html' %}
{% load static %}

{% block title %}Inicio | Unisalud{% endblock %}

{% block content %}
<!-- <div class="inicio-container" style="padding: 80px 20px;">
    <div class="text-center">
        <h1>Bienvenido a Unisalud</h1>
        <p>Su plataforma de salud confiable, accesible y segura.</p>
    </div>
    <div class="container my-5">
        <div class="row align-items-center">
            <div class="col-md-7 mb-4 mb-md-0">
                <img src="{% static 'img/imageninicio.jpg' %}" 
                    class="img-fluid rounded-3 shadow-lg"
                    id="imageninicio">
            </div>
            <div class="col-md-5 d-flex flex-column align-items-center">
                <a href="{% url 'login-us' %}" class="btn btn-primary btn-lg w-75 mb-4" role="button">
                    Soy Paciente
                </a>
                <a href="{% url 'login_prof_salud' %}" class="btn btn-outline-primary btn-lg w-75" role="button">
                    Soy Profesional
                </a>
                <a href="{% url 'login_admin' %}" class="btn btn-outline-primary btn-lg w-75" role="button">
                    Soy Administrativo
                </a>
            </div>
        </div>
            <div class="col-md-7 mb-4 mb-md-0">
                <div style="margin-top: auto;">
                    <img src="{% static 'img/imageninicio.png' %}" alt="Imagen de salud" 
                    style="width: 100%; height: auto; border-radius: 10px; box-shadow: 0 4px 8px rgba(55,0,0,0.55);">
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

def inicio_unisalud(request):
    if request.user.is_authenticated:
        if request.user.is_paciente:
            return redirect('inicio_paciente')
        elif request.user.is_profesional:
            return redirect('inicio_profesionalS')
        elif request.user.is_admin:
            return redirect('inicio_admin')
    return render(request, 'paginas/inicio_unisalud.html')
    
    path('', views.inicio_unisalud, name='inicio_unisalud'),
    url unisalud     path('', usuario_views.inicio_unisalud, name='inicio_unisalud'),  -->
Es de anotar que esta se retira,se elimina porque al ingresar el PACIENTE o el PROF-SALUD o el ADMINISTRADOR, debe aparecer el login--> alli deberá estar el registro de los roles
________________________________________________________________________
8 de NOVIEMBRE DEL 2025
CONEXION BD Unisalud
Se inicia con la conexión de la BD  de unisalud, siguiendo las instrucciones dadas en clase:
1. pip install pymysql
2. pip install cryptography :para seguridad en cifrado
3. settings: Databases:
'default': {
    	'ENGINE': 'django.db.backends.mysql',
    	'NAME': '',  # Nombre de la BD
    	'USER': 'root',  # Usuario de MySQL
    	'PASSWORD': 'tu_contraseña',  # Cambia por tu contraseña
    	'HOST': 'localhost',  # Servidor de BD
   	    'PORT': '3306',  # Puerto de MySQL (por defecto)
    }
4. en _init_py : import pymysql
                pymysql.install_as_mysqldb()
5. python manage.py runserver
6. sale "18 cosas" --> python manage.py migrate --> en BD de mySQL salen las "18 cosas"
7. python manage.py runserver
8. Para verificar conexión: python manage.py check --database default
AGREGAR TABLAS A MODELS
En la terminal: python manage.py inspectdb xxxx xxxx xxxx xxxx>.\aplication\models.py

