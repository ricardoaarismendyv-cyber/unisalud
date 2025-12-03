from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuario.models import Turnos  

@login_required
def inicio_turnero(request):
    return render(request, "turnero/inicio_turnos.html")


@login_required
def gestionar_turnero(request):
    turnos = Turnos.objects.filter(estado__in=["pendiente", "llamando"]).order_by("id_turno")
    return render(request, "turnero/gestionar_turnero.html", {"turnos": turnos})


@login_required
def llamar_turno(request, id_turno):
    turno = get_object_or_404(Turnos, id_turno=id_turno)
    turno.estado = "llamando"
    turno.save()
    return redirect("gestionar_turnos")


@login_required
def cerrar_turno(request, id_turno):
    turno = get_object_or_404(Turnos, id_turno=id_turno)
    turno.estado = "cerrado"
    turno.save()
    return redirect("gestionar_turnos")

@login_required
def pantalla_turnos(request):
    # Turno actual (el que se está llamando)
    turno_actual = Turnos.objects.filter(estado="llamando").order_by("-id_turno").first()

    # Historial (los últimos turnos cerrados)
    historial = Turnos.objects.filter(estado="cerrado").order_by("-id_turno")[:10]

    return render(request, "turnero/pantalla_turnos.html", {
        "turno_actual": turno_actual,
        "historial": historial,
    })
