# Generated by Django 4.1.3 on 2022-11-08 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0002_alter_address_options_alter_contacts_options_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
    ]
