from django.shortcuts import render, get_object_or_404


# Create your views here.


def inicio(request):
    return render(request, 'paginas/inicio.html' )
