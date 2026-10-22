from django.contrib import admin
from django.test import TestCase
from django.urls import reverse

from .admin import CategoriaAdmin, JuegoAdmin
from .models import Categoria, Juego


class CatalogoViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.categoria = Categoria.objects.create(
            nombre="Aventura",
            descripcion="Juegos de aventura",
        )
        cls.juego = Juego.objects.create(
            categoria=cls.categoria,
            nombre="Juego de prueba",
            descripcion="Descripción del juego",
            plataforma="PC",
            precio=19990,
            stock=5,
        )

    def test_inicio_muestra_juegos_disponibles_del_orm(self):
        response = self.client.get(reverse("catalogo:inicio"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Juego de prueba")
        self.assertContains(response, "Aventura")
        self.assertContains(response, "$19.990")
        self.assertContains(response, reverse("catalogo:detalle", args=[self.juego.slug]))

    def test_inicio_muestra_estado_vacio(self):
        Juego.objects.all().delete()

        response = self.client.get(reverse("catalogo:inicio"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aún no hay juegos disponibles")

    def test_detalle_muestra_juego_y_categoria(self):
        response = self.client.get(reverse("catalogo:detalle", args=[self.juego.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Juego de prueba")
        self.assertContains(response, "Aventura")
        self.assertContains(response, "$19.990")

    def test_imagen_del_juego_se_muestra_en_catalogo_y_detalle(self):
        self.juego.imagen = "juegos/portada.jpg"
        self.juego.save(update_fields=["imagen"])

        catalogo_response = self.client.get(reverse("catalogo:inicio"))
        detalle_response = self.client.get(reverse("catalogo:detalle", args=[self.juego.slug]))

        self.assertContains(catalogo_response, "/media/juegos/portada.jpg")
        self.assertContains(detalle_response, "/media/juegos/portada.jpg")

    def test_id_inexistente_muestra_pagina_404_personalizada(self):
        response = self.client.get(reverse("catalogo:detalle", args=["juego-inexistente"]))

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "No encontramos ese juego", status_code=404)
        self.assertContains(response, "Volver al inicio", status_code=404)
        self.assertContains(response, "Ver catálogo", status_code=404)

    def test_juego_no_disponible_no_se_publica(self):
        self.juego.disponible = False
        self.juego.save()

        response = self.client.get(reverse("catalogo:inicio"))

        self.assertNotContains(response, "Juego de prueba")

    def test_juego_no_disponible_muestra_pagina_404_personalizada(self):
        self.juego.disponible = False
        self.juego.save()

        response = self.client.get(reverse("catalogo:detalle", args=[self.juego.slug]))

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "No encontramos ese juego", status_code=404)
        self.assertContains(response, "Volver al inicio", status_code=404)
        self.assertContains(response, "Ver catálogo", status_code=404)

    def test_modelos_registrados_y_categoria_tiene_inline(self):
        self.assertIn(Categoria, admin.site._registry)
        self.assertIn(Juego, admin.site._registry)
        categoria_admin = admin.site._registry[Categoria]
        self.assertIsInstance(categoria_admin, CategoriaAdmin)
        self.assertTrue(categoria_admin.inlines)
        self.assertTrue(issubclass(categoria_admin.inlines[0], admin.TabularInline))

    def test_admin_muestra_miniatura_de_imagen_del_juego(self):
        juego_admin = JuegoAdmin(Juego, admin.site)
        self.juego.imagen = "juegos/portada.jpg"

        html = str(juego_admin.miniatura(self.juego))

        self.assertIn('<img src="/media/juegos/portada.jpg"', html)
        self.assertIn('alt="Portada de Juego de prueba"', html)
        self.assertIn("miniatura", juego_admin.get_list_display(None))


class CatalogoModelsTests(TestCase):
    def test_modelos_tienen_representacion_legible_y_relacion_inversa(self):
        categoria = Categoria.objects.create(nombre="Estrategia")
        juego = Juego.objects.create(
            categoria=categoria,
            nombre="Juego de estrategia",
            precio=10000,
        )

        self.assertEqual(str(categoria), "Estrategia")
        self.assertEqual(str(juego), "Juego de estrategia")
        self.assertEqual(categoria.juegos.get(), juego)

    def test_slug_se_genera_desde_el_nombre_y_evitar_repeticiones(self):
        categoria = Categoria.objects.create(nombre="Acción")
        primer_juego = Juego.objects.create(
            categoria=categoria,
            nombre="Aventura épica",
            precio=10000,
        )
        segundo_juego = Juego.objects.create(
            categoria=categoria,
            nombre="Aventura épica",
            precio=12000,
        )

        self.assertEqual(primer_juego.slug, "aventura-epica")
        self.assertEqual(segundo_juego.slug, "aventura-epica-2")
