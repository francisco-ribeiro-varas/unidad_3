from django.db import models
from django.utils.text import slugify


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
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    plataforma = models.CharField(max_length=80, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "juego"
        verbose_name_plural = "juegos"

    def save(self, *args, **kwargs):
        base_slug = slugify(self.nombre) or "juego"
        slug = base_slug
        suffix = 2
        juegos_con_slug = type(self).objects.all()
        if self.pk:
            juegos_con_slug = juegos_con_slug.exclude(pk=self.pk)

        while juegos_con_slug.filter(slug=slug).exists():
            slug = f"{base_slug[:140]}-{suffix}"
            suffix += 1

        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
