from django.shortcuts import get_object_or_404, render

from .models import Juego


def inicio(request):
    juegos = Juego.objects.filter(disponible=True).select_related("categoria")
    return render(request, "catalogo/index.html", {"juegos": juegos})


def detalle_juego(request, pk):
    juego = get_object_or_404(
        Juego.objects.select_related("categoria"),
        pk=pk,
        disponible=True,
    )
    return render(request, "catalogo/detalle.html", {"juego": juego})
