from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext
from src.entities.models import Entity, Contacts, Address
from src.entities.tasks import make_debt_zero_worker


class EntityAdmin(admin.ModelAdmin):
    """ Configuration for Entity admin model. """

    list_display = ('name', 'id', 'type', 'get_href', 'debt', 'date_created', 'get_city')
    search_fields = ('name', 'id', 'type', 'provider', 'date_created', 'contacts__address__city')
    list_filter = ('contacts__address__city',)
    fields = ('name', 'type', 'provider', 'get_href', 'debt', 'products', 'date_created')
    readonly_fields = ('get_href', 'date_created')
    filter_horizontal = ('products',)
    actions = ('make_debt_zero',)

    def save_model(self, request, obj, form, change) -> None:
        """ Overwritten save_model method. Validates or not entity's/provider's type. """

        if obj.provider is None:
            super().save_model(request, obj, form, change)
            return

        elif obj.type <= obj.provider.type:
            messages.set_level(request, messages.ERROR)
            messages.error(request, "Cannot specify a provider if it's lower or equal in the hierarchy.")

        else:
            super().save_model(request, obj, form, change)

        return

    @admin.action(description="Make selected entities' debt as 0")
    def make_debt_zero(self, request, queryset) -> None:
        """
        Admin action which makes selected entities' debts as 0.
        If selected Entities >= 20 theirs debts will set to 0 async.
        """

        if queryset.count() >= 20:
            make_debt_zero_worker.delay(list(queryset.values('id')))
            self.message_user(request, "Selected debts were successfully marked as 0.", messages.SUCCESS)
            return

        updated = queryset.update(debt=0.00)
        self.message_user(request, ngettext(
            "%d debt was successfully marked as 0.",
            "%d debts were successfully marked as 0.",
            updated,
        ) % updated, messages.SUCCESS)

    def get_href(self, obj) -> mark_safe or None:
        """ Creates new element of field list, contains href to entity's provider. """

        if obj.provider:
            return mark_safe(
                f"<a href='/admin/entities/entity/{obj.provider.id}/change/'>"
                f"{obj.provider}"
                f"</a>"
            )

    def get_city(self, obj) -> str:
        """ Returns entity's city from Address model. """

        return obj.contacts.address.city

    get_href.short_description = 'Provider (clickable)'
    get_city.admin_order_field = 'city'
    get_city.short_description = 'City'


class ContactsAdmin(admin.ModelAdmin):
    """ Configuration for Contacts admin model. """

    list_display = ('entity', 'email')
    search_fields = ('entity', 'email', 'address__city')


class AddressAdmin(admin.ModelAdmin):
    """ Configuration for Address admin model. """

    list_display = ('contacts', 'country', 'city', 'street', 'house')
    search_fields = ('contacts', 'country', 'city', 'street', 'house')


admin.site.register(Entity, EntityAdmin)
admin.site.register(Contacts, ContactsAdmin)
admin.site.register(Address, AddressAdmin)
