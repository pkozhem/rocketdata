from django.db import migrations


def populate_entity_products(apps, schema_editor) -> None:
    """ Creates relation for products for existing Entities. """

    Entity = apps.get_model('entities', 'Entity')
    Product = apps.get_model('products', 'Product')

    Entity.objects.get(name='Crystal').products.add(Product.objects.get(name='iPhone 11'))
    Entity.objects.get(name='Crystal').products.add(Product.objects.get(name='Lamp'))
    Entity.objects.get(name='Crystal').save()

    Entity.objects.get(name='AMI').products.add(Product.objects.get(name='Sofa'))
    Entity.objects.get(name='AMI').products.add(Product.objects.get(name='Table'))
    Entity.objects.get(name='AMI').save()

    Entity.objects.get(name='MaxShop').products.add(Product.objects.get(name='iPhone 11'))
    Entity.objects.get(name='MaxShop').products.add(Product.objects.get(name='Sofa'))
    Entity.objects.get(name='MaxShop').save()


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0004_auto_20221112_add_addresses'),
        ('products', '0002_auto_20221112_add_products')
    ]

    operations = [
        migrations.RunPython(populate_entity_products)
    ]
