from django.db import migrations


def populate_models(apps, schema_editor):
    # We can't import the models directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Bread = apps.get_model("breakfasts", "Bread")
    Base = apps.get_model("breakfasts", "Base")
    Ingredient = apps.get_model("breakfasts", "Ingredient")
    Drink = apps.get_model("breakfasts", "Drink")

    mollete, mollete_created = Bread.objects.get_or_create(name="Mollete")
    andaluza, andaluza_created = Bread.objects.get_or_create(name="Andaluza")
    viena, viena_created = Bread.objects.get_or_create(name="Viena")
    bollo, bollo_created = Bread.objects.get_or_create(name="Bollo")

    aceite, aceite_created = Base.objects.get_or_create(name="Aceite")
    mantequilla, mantequilla_created = Base.objects.get_or_create(name="Mantequilla")
    pate, pate_created = Base.objects.get_or_create(name="Paté")
    sobrasada, sobrasada_created = Base.objects.get_or_create(name="Sobrasada")
    manteca, manteca_created = Base.objects.get_or_create(name="Manteca Colorá")

    tomate_rodajas, tomate_rodajas_created = Ingredient.objects.get_or_create(name="Tomate en Rodajas")
    tomate_triturado, tomate_triturado_created = Ingredient.objects.get_or_create(name="Tomate Triturado")
    jamon, jamon_created = Ingredient.objects.get_or_create(name="Jamón Serrano")
    york, york_created = Ingredient.objects.get_or_create(name="Jamón York")
    mecha, mecha_created = Ingredient.objects.get_or_create(name="Carne Mechá")
    queso, queso_created = Ingredient.objects.get_or_create(name="Queso Viejo")
    loncha, loncha_created = Ingredient.objects.get_or_create(name="Queso en Lonchas")

    solo, solo_created = Drink.objects.get_or_create(name="Café Solo")
    leche, leche_created = Drink.objects.get_or_create(name="Café con Leche")
    cortado, cortado_created = Drink.objects.get_or_create(name="Café Cortado")
    colacao, colacao_created = Drink.objects.get_or_create(name="Cola Cao")
    batido, batido_created = Drink.objects.get_or_create(name="Batido de Chocolate")
    te, te_created = Drink.objects.get_or_create(name="Té")


class Migration(migrations.Migration):

    dependencies = [("breakfasts", "0001_initial")]

    operations = [
        # We set `reverse_code` to `noop` because we cannot revert the
        # migration to get it back in the previous state.
        # If `reverse_code` is not given, the migration will not be
        # reversible, which is not the behaviour we expect here.
        migrations.RunPython(populate_models, reverse_code=migrations.RunPython.noop)
    ]
