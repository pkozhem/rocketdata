from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    """ Configuration for User admin model. """

    list_display = UserAdmin.list_display + ('entity',)
    search_fields = UserAdmin.search_fields + ('entity__name',)
    fieldsets = UserAdmin.fieldsets + (
        ('Employer', {
            'fields': ('entity',)
        }),
    )
