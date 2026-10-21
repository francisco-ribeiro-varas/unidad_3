from django.db import migrations, models
from django.utils.text import slugify


def crear_slugs(apps, schema_editor):
    Juego = apps.get_model("catalogo", "Juego")
    for juego in Juego.objects.order_by("pk"):
        base_slug = slugify(juego.nombre)[:150] or f"juego-{juego.pk}"
        slug = base_slug
        suffix = 2
        while Juego.objects.filter(slug=slug).exclude(pk=juego.pk).exists():
            slug = f"{base_slug[:140]}-{suffix}"
            suffix += 1
        juego.slug = slug
        juego.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("catalogo", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="juego",
            name="slug",
            field=models.SlugField(blank=True, max_length=150, null=True),
        ),
        migrations.RunPython(crear_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="juego",
            name="slug",
            field=models.SlugField(blank=True, max_length=150, unique=True),
        ),
    ]
