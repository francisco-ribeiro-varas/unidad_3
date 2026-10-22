from django.contrib import admin
from django.utils.html import format_html

from .models import Categoria, Juego


class JuegoInline(admin.TabularInline):
    model = Juego
    extra = 1


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activa")
    list_filter = ("activa",)
    search_fields = ("nombre", "descripcion")
    ordering = ("nombre",)
    inlines = (JuegoInline,)


@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "plataforma", "precio_formateado", "stock", "miniatura", "disponible")
    list_filter = ("categoria", "plataforma", "disponible")
    search_fields = ("nombre", "descripcion", "plataforma", "categoria__nombre")
    ordering = ("nombre",)
    readonly_fields = ("slug",)

    @admin.display(description="Imagen")
    def miniatura(self, obj):
        if not obj.imagen:
            return "Sin imagen"
        return format_html(
            '<img src="{}" alt="Portada de {}" style="width: 80px; height: auto;">',
            obj.imagen.url,
            obj.nombre,
        )

    @admin.display(description="Precio", ordering="precio")
    def precio_formateado(self, obj):
        return f"${obj.precio:,.0f}".replace(",", ".")


admin.site.site_header = "Administración de Tienda de juegos"
admin.site.site_title = "Tienda de juegos"
admin.site.index_title = "Gestión del catálogo"
