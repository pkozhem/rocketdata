from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from src.entities.models import Entity, Contacts, Address

User = get_user_model()


@receiver(post_save, sender=Entity)
def create_contacts_and_address(sender, instance, created, **kwargs):
    """ Auto create Contacts and Address when Entity is created. """

    if created:
        Contacts.objects.create(entity=instance)
        Address.objects.create(contacts=instance.contacts)


@receiver(post_save, sender=Entity)
def create_contacts_and_address(sender, instance, **kwargs):
    """ Saves incoming data for Contacts and Address instantly . """

    instance.contacts.save()
    instance.contacts.address.save()
