from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserPublicSerializer(serializers.ModelSerializer):
    """ Public User serializer. """

    class Meta:
        model = User
        exclude = (
            "password",
            "email",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser"
        )
