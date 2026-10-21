from django.urls import path

from . import views

app_name = "catalogo"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("juegos/<int:pk>/", views.detalle_juego, name="detalle"),
]
