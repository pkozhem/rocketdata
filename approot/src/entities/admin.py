from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext
from src.entities.models import Entity, Contacts, Address


class EntityAdmin(admin.ModelAdmin):
    """ Configuring Entity admin model. """

    list_display = ('name', 'type', 'get_href', 'debt', 'date_created', 'get_city')
    search_fields = ('name', 'type', 'provider', 'date_created', 'contacts__address__city')
    list_filter = ('contacts__address__city',)
    fields = ('type', 'name', 'provider', 'get_href', 'debt', 'products')
    readonly_fields = ('get_href',)
    filter_horizontal = ('products',)
    actions = ('make_debt_zero',)

    def save_model(self, request, obj, form, change):
        """ Makes unavailable to specify a provider if it's lower or equal in the hierarchy. """

        if obj.provider is None:
            obj.save()
            super().save_model(request, obj, form, change)
            return

        if obj.type <= obj.provider.type:
            messages.set_level(request, messages.ERROR)
            messages.error(request, "Cannot specify a provider if it's lower in the hierarchy.")
        else:
            obj.save()
            super().save_model(request, obj, form, change)

        return

    @admin.action(description="Make selected entities' debt as 0")
    def make_debt_zero(self, request, queryset):
        """ Admin action which makes selected entities' debts as 0. """

        updated = queryset.update(debt=0.00)
        self.message_user(request, ngettext(
            "%d debt was successfully marked as 0.",
            "%d debts were successfully marked as 0.",
            updated,
        ) % updated, messages.SUCCESS)

    def get_href(self, obj):
        """ Creates new element of field list, contains href to entity's provider. """

        if obj.provider:
            return mark_safe(
                f"<a href='/admin/entities/entity/{obj.provider.id}/change/'>"
                f"{obj.provider}"
                f"</a>"
            )

    def get_city(self, obj):
        """ Returns entity's city from Address model. """

        return obj.contacts.address.city

    get_href.short_description = 'Provider (clickable)'
    get_city.admin_order_field = 'city'
    get_city.short_description = 'City'


class ContactsAdmin(admin.ModelAdmin):
    """ Configuring Contacts admin model. """

    list_display = ('entity', 'email')
    search_fields = ('entity', 'email', 'address__city')


class AddressAdmin(admin.ModelAdmin):
    """ Configuring Address admin model. """

    list_display = ('contacts', 'country', 'city', 'street', 'house')
    search_fields = ('contacts', 'country', 'city', 'street', 'house')


admin.site.register(Entity, EntityAdmin)
admin.site.register(Contacts, ContactsAdmin)
admin.site.register(Address, AddressAdmin)
