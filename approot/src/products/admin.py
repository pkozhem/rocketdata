from django.contrib import admin
from src.products.models import Product


class ProductAdmin(admin.ModelAdmin):
    """ Configuring display list and search fields of Product model in Admin panel. """

    list_display = ('name', 'model', 'date_release', 'entity')
    search_fields = ('name', 'date_release', 'entity')


admin.site.register(Product, ProductAdmin)
