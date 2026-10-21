from django.contrib import admin

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
    list_display = ("nombre", "categoria", "plataforma", "precio", "stock", "disponible")
    list_filter = ("categoria", "plataforma", "disponible")
    search_fields = ("nombre", "descripcion", "plataforma", "categoria__nombre")
    ordering = ("nombre",)
    readonly_fields = ("slug",)


admin.site.site_header = "Administración de Tienda de juegos"
admin.site.site_title = "Tienda de juegos"
admin.site.index_title = "Gestión del catálogo"
