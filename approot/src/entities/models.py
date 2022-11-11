from django.db import models
from django.core.exceptions import ValidationError
from src.products.models import Product


class Entity(models.Model):
    """ Entity model. """

    TYPES = (
        (0, 'Factory'),
        (1, 'Distributor'),
        (2, 'Dealership'),
        (3, 'Retail network'),
        (4, 'Entrepreneur')
    )
    type = models.PositiveSmallIntegerField(default=0, null=True, blank=True, choices=TYPES)
    name = models.CharField(blank=True, null=True, unique=True, max_length=256)
    products = models.ManyToManyField(Product, default=None, related_name='entity', blank=True)
    provider = models.ForeignKey('self', related_name='parent', null=True, blank=True, on_delete=models.SET_NULL)
    debt = models.DecimalField(default=0, null=True, blank=True, max_digits=9, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Entity'
        verbose_name_plural = 'Entities'

    def clean(self) -> None:
        """ Overwritten clean method. Validates or not entity's/provider's type. """

        if self.provider is None:
            super().clean()
            return

        if self.type <= self.provider.type:
            raise ValidationError("Cannot specify a provider if it's lower or equal in the hierarchy.")
        super().clean()

    def __str__(self):
        return f'{self.name}'


class Contacts(models.Model):
    """ Contacts model. """

    email = models.EmailField(blank=True, null=True, unique=True, max_length=256)
    entity = models.OneToOneField(Entity, related_name='contacts', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Contacts'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return f'{self.entity}'


class Address(models.Model):
    """ Address model. """

    country = models.CharField(default='Belarus', null=True, blank=True, max_length=56)
    city = models.CharField(default='Minsk', null=True, blank=True, max_length=85)
    street = models.CharField(default='Victory', null=True, blank=True, max_length=60)
    house = models.PositiveSmallIntegerField(default=1, null=True, blank=True)
    contacts = models.OneToOneField(Contacts, related_name='address', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'{self.contacts}'
