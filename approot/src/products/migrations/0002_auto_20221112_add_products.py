from datetime import date
from django.db import migrations


def populate_products(apps, schema_editor) -> None:
    """ Creates Products. """

    Product = apps.get_model('products', 'Product')

    Product.objects.create(name='Sofa', model='Black', date_release=date(2022, 11, 9))
    Product.objects.create(name='iPhone 11', model='64 GB', date_release=date(2022, 11, 10))
    Product.objects.create(name='Lamp', model='LED', date_release=date(2022, 11, 11))
    Product.objects.create(name='Table', model='Oak', date_release=date(2022, 11, 12))


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('entities', '0004_auto_20221112_add_addresses')
    ]

    operations = [
        migrations.RunPython(populate_products)
    ]
