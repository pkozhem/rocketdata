from django.db import models


class Product(models.Model):
    """ Product model. """

    name = models.CharField(null=True, blank=True, max_length=256)
    model = models.CharField(null=True, blank=True, max_length=128)
    date_release = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'{self.name}'
