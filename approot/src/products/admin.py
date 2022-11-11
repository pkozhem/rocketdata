from django.contrib import admin
from src.products.models import Product


class ProductAdmin(admin.ModelAdmin):
    """ Configuration for Product admin model. """

    list_display = ('name', 'id', 'model', 'date_release')
    search_fields = ('name', 'id', 'date_release')
    fields = ('name', 'model', 'date_release')


admin.site.register(Product, ProductAdmin)
