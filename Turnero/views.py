from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuario.models import Turnos, Usuarios, ProfesionalSalud
from django.contrib import messages



def inicio_turnero(request):
    id_prof = request.session.get('id_profesional')

    profesional = None
    if id_prof:
        profesional = ProfesionalSalud.objects.get(id_profesional=id_prof)

    return render(request, "turnero/inicio_turnos.html", {
        'profesional': profesional
    })



def gestionar_turnero(request):
    turnos = Turnos.objects.filter(
        estado__in=["pendiente", "llamando", "cerrado"]
    ).order_by("id_turno")

    return render(request, "turnero/gestionar_turnero.html", {"turnos": turnos})




def llamar_turno(request, id_turno):
    turno = get_object_or_404(Turnos, id_turno=id_turno)

    # Obtener profesional que está logueado
    id_profesional = request.session.get("id_profesional")

    if id_profesional:
        turno.id_profesional_id = id_profesional  # Asignar profesional

    turno.estado = "llamando"
    turno.save()

    return redirect("gestionar_turnos")



def cerrar_turno(request, id_turno):
    turno = get_object_or_404(Turnos, id_turno=id_turno)
    turno.estado = "cerrado"
    turno.save()
    return redirect("gestionar_turnos")


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


def volver_llamar(request, id_turno):
    turno = get_object_or_404(Turnos, id_turno=id_turno)

    id_profesional = request.session.get("id_profesional")
    if id_profesional:
        turno.id_profesional_id = id_profesional

    turno.estado = "llamando"
    turno.save()

    return redirect("gestionar_turnos")


