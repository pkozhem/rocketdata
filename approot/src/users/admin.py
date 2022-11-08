from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    """ Configuring display list and search fields of Product model in Admin panel. """

    list_display = UserAdmin.list_display + ('entity',)
    search_fields = UserAdmin.search_fields + ('entity__name',)
    fieldsets = UserAdmin.fieldsets + (
        ('Employer', {
            'fields': ('entity',)
        }),
    )
