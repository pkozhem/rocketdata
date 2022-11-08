from django.db import models


class Entity(models.Model):
    """ Entity model. """

    TYPES = (
        ('Factory', 'Factory'),
        ('Distributor', 'Distributor'),
        ('Dealership', 'Dealership'),
        ('Retail network', 'Retail network'),
        ('Entrepreneur', 'Entrepreneur')
    )
    type = models.CharField(default='Entrepreneur', max_length=14, choices=TYPES)
    name = models.CharField(blank=True, null=True, unique=True, max_length=256)
    # provider = models.OneToOneField()
    debt = models.DecimalField(default=0, null=True, blank=True, max_digits=9, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Entity'
        verbose_name_plural = 'Entities'

    def __str__(self):
        return f'{self.name}'


class Contacts(models.Model):
    """ Contacts model. One to one field to Entity instance. """

    email = models.EmailField(blank=True, null=True, unique=True, max_length=256)
    entity = models.OneToOneField(Entity, related_name='contacts', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Contacts'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return f'{self.entity}'


class Address(models.Model):
    """ Address model. One to one field to Contacts instance. """

    country = models.CharField(default='Belarus', null=True, blank=True, max_length=56)
    city = models.CharField(default='Minsk', null=True, blank=True, max_length=85)
    street = models.CharField(default='Victory', null=True, blank=True, max_length=60)
    house = models.PositiveIntegerField(default='1', null=True, blank=True)
    contacts = models.OneToOneField(Contacts, related_name='address', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'{self.contacts}'
