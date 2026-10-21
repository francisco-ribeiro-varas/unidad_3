from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Juego


def inicio(request):
    juegos = Juego.objects.filter(disponible=True).select_related("categoria")
    return render(request, "catalogo/index.html", {"juegos": juegos})


def detalle_juego(request, slug):
    try:
        juego = get_object_or_404(
            Juego.objects.select_related("categoria"),
            slug=slug,
            disponible=True,
        )
    except Http404:
        return render(request, "404.html", status=404)

    return render(request, "catalogo/detalle.html", {"juego": juego})
