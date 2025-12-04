from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuario.models import Turnos  
from django.contrib import messages


@login_required
def inicio_turnero(request):
    return render(request, "turnero/inicio_turnos.html")


@login_required
def gestionar_turnero(request):
    turnos = Turnos.objects.filter(
        estado__in=["pendiente", "llamando", "cerrado"]
    ).order_by("id_turno")

    # Normalizar estado para evitar problemas en el template
    for t in turnos:
        if t.estado:
            t.estado = t.estado.lower().strip()

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

    turno_actual = (
    Turnos.objects
    .filter(estado__iregex=r"^llam")
    .order_by("-id_turno")
)



    turno_siguiente = (
        Turnos.objects
        .filter(estado__icontains="pend")
        .order_by("id_turno")
        .first()
    )

    historial = (
        Turnos.objects
        .filter(estado__icontains="cerr")
        .order_by("-id_turno")[:20]
    )

    return render(request, "turnero/pantalla_turnos.html", {
        "turno_actual": turno_actual,
        "turno_siguiente": turno_siguiente,
        "historial": historial,
    })

@login_required
def volver_llamar(request, id_turno):
    turno = get_object_or_404(Turnos, id_turno=id_turno)

    turno.estado = "llamando"
    turno.save()

    messages.success(request, f"El turno {turno.letra}{turno.numero} fue vuelto a llamar.")
    return redirect("gestionar_turnos")

