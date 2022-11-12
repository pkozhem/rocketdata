from django.db import migrations


def populate_address(apps, schema_editor) -> None:
    """ Creates relations for contacts for existing Contacts """

    Address = apps.get_model('entities', 'Address')
    Contacts = apps.get_model('entities', 'Contacts')

    Address.objects.create(
        country='Norway',
        city='Oslo',
        contacts=Contacts.objects.get(entity__name='Crystal')
    )
    Address.objects.create(
        contacts=Contacts.objects.get(entity__name='AMI')
    )
    Address.objects.create(
        country='Poland',
        city='Warsaw',
        street='Airport',
        house=12,
        contacts=Contacts.objects.get(entity__name='MaxShop')
    )
    Address.objects.create(
        country='Germany',
        city='Berlin',
        street='Mein',
        house=13,
        contacts=Contacts.objects.get(entity__name='Adidas')
    )


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0003_auto_20221112_add_providers_contacts'),
    ]

    operations = [
        migrations.RunPython(populate_address)
    ]
