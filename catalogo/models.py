from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "categoría"
        verbose_name_plural = "categorías"

    def __str__(self):
        return self.nombre


class Juego(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="juegos",
    )
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    plataforma = models.CharField(max_length=80, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "juego"
        verbose_name_plural = "juegos"

    def __str__(self):
        return self.nombre
