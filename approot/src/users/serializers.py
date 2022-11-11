from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserPrivateSerializer(serializers.ModelSerializer):
    """ Private User serializer. """

    class Meta:
        model = User
        fields = '__all__'


class UserPublicSerializer(serializers.ModelSerializer):
    """ Public User serializer. """

    class Meta:
        model = User
        fields = ('id', 'username', 'is_active')
        extra_kwargs = {
            "username":
                {
                    "read_only": True
                }
        }
