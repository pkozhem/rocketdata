from django.contrib import admin, messages
from django.utils.translation import ngettext
from src.entities.models import Entity, Contacts, Address


class EntityAdmin(admin.ModelAdmin):
    """ Configuring display list, search fields and filter list of Entity model in Admin panel. """

    list_display = ('name', 'type', 'debt', 'date_created', 'get_city')
    search_fields = ('name', 'type', 'date_created', 'contacts__address__city')
    list_filter = ('contacts__address__city',)
    actions = ('make_debt_zero',)

    @admin.action(description="Make selected entities' debt as 0")
    def make_debt_zero(self, request, queryset):
        """ Admin action which makes selected entities' debts as 0. """

        updated = queryset.update(debt=0.00)
        self.message_user(request, ngettext(
            "%d debt was successfully marked as 0.",
            "%d debts were successfully marked as 0.",
            updated,
        ) % updated, messages.SUCCESS)

    def get_city(self, obj):
        return obj.contacts.address.city

    get_city.admin_order_field = 'city'
    get_city.short_description = 'City'


class ContactsAdmin(admin.ModelAdmin):
    """ Configuring display list and search fields of Contacts model in Admin panel. """

    list_display = ('entity', 'email')
    search_fields = ('entity', 'email', 'address__city')


class AddressAdmin(admin.ModelAdmin):
    """ Configuring display list and search fields of Address model in Admin panel. """

    list_display = ('contacts', 'country', 'city', 'street', 'house')
    search_fields = ('contacts', 'country', 'city', 'street', 'house')


admin.site.register(Entity, EntityAdmin)
admin.site.register(Contacts, ContactsAdmin)
admin.site.register(Address, AddressAdmin)
