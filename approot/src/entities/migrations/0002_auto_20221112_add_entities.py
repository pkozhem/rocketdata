from django.db import migrations


def populate_entities(apps, schema_editor) -> None:
    """ Creates few Entities. """

    Entity = apps.get_model('entities', 'Entity')

    Entity.objects.create(type=0, name='Crystal')
    Entity.objects.create(type=0, name='AMI')
    Entity.objects.create(type=4, name='MaxShop')
    Entity.objects.create(type=2, name='Adidas')


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_entities)
    ]
