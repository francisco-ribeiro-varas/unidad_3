from django.urls import path

from . import views

app_name = "catalogo"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("juegos/<slug:slug>/", views.detalle_juego, name="detalle"),
]
