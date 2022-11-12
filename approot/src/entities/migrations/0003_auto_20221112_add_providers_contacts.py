from django.db import migrations


def populate_contacts_and_provider(apps, schema_editor) -> None:
    """
    Creates relations for provider FK for existing Entities.
    Creates relations for entity for new Contacts.
    """

    Contacts = apps.get_model('entities', 'Contacts')
    Entity = apps.get_model('entities', 'Entity')

    MaxShop = Entity.objects.get(name='MaxShop')
    MaxShop.provider = Entity.objects.get(name='Crystal')
    MaxShop.save()

    Adidas = Entity.objects.get(name='Adidas')
    Adidas.provider = Entity.objects.get(name='AMI')
    Adidas.save()

    Contacts.objects.create(email='crystal@gmail.com', entity=Entity.objects.get(name='Crystal'))
    Contacts.objects.create(email='ami@gmail.com', entity=Entity.objects.get(name='AMI'))
    Contacts.objects.create(email='maxshop@gmail.com', entity=MaxShop)
    Contacts.objects.create(email='adidas@gmail.com', entity=Adidas)


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0002_auto_20221112_add_entities'),
    ]

    operations = [
        migrations.RunPython(populate_contacts_and_provider)
    ]
