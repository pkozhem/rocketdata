from django.db import migrations


def populate_users(apps, schema_editor) -> None:
    """ Creates Users. """

    User = apps.get_model('users', 'User')
    Entity = apps.get_model('entities', 'Entity')

    User.objects.create(username='Anna', password='qwerty123', entity=Entity.objects.get(name='Crystal'))
    User.objects.create(username='Pavel', password='qwerty123', entity=Entity.objects.get(name='AMI'))
    User.objects.create(username='William', password='qwerty123', entity=Entity.objects.get(name='Adidas'))


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('entities', '0004_auto_20221112_add_addresses')
    ]

    operations = [
        migrations.RunPython(populate_users)
    ]
