from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from drf_writable_nested import WritableNestedModelSerializer
from src.entities.models import Entity, Contacts, Address
from src.products.serializers import ProductSerializer
from src.users.serializers import UserPublicSerializer


class AddressSerializer(serializers.ModelSerializer):
    """ Address serializer. """

    class Meta:
        model = Address
        exclude = ('id', 'contacts')


class ContactsSerializer(WritableNestedModelSerializer):
    """ Contacts serializer. Makes possible updating and creating nested models. """

    email = serializers.EmailField(required=False)
    address = AddressSerializer(many=False, required=False)

    class Meta:
        model = Contacts
        exclude = ('id', 'entity')


class EntitySerializer(WritableNestedModelSerializer):
    """ Entity serializer. Makes possible updating and creating nested. """

    contacts = ContactsSerializer(many=False, required=False)
    products = ProductSerializer(many=True, required=False, read_only=True)
    user = UserPublicSerializer(many=True, required=False)

    class Meta:
        model = Entity
        fields = '__all__'
        extra_kwargs = {
            "type": {
                "required": True
            },
            "name": {
                "required": True
            },
            "debt": {
                "read_only": True
            },
            "date_created": {
                "read_only": True
            }
        }

    def get_provider_type(self) -> int or None:
        """ Returns Entity provider's type, None if it doesn't exist. """

        provider_name: str or None = self.validated_data.get('provider')

        return None if provider_name is None \
            else list(Entity.objects.filter(name=provider_name).values('type'))[0].get('type')

    def validate(self, attrs):
        """ Validates or not incoming name length. """

        if len(attrs['name']) > 50:
            raise ValidationError({"detail": "Entity's name should contains maximum 50 symbols."})

        return attrs

    def create(self, validated_data):
        """ Overwritten save method. Validates or not entity's/provider's type. """

        provider_type = self.get_provider_type()

        if provider_type is None:
            entity = super(EntitySerializer, self).create(validated_data)
            return entity

        elif validated_data.get('type') <= provider_type:
            raise ValidationError({"detail": "Cannot specify a provider if it's lower or equal in the hierarchy."})

        entity = super(EntitySerializer, self).create(validated_data)
        return entity

    def update(self, instance, validated_data):
        """ Overwritten update method. Validates or not entity's/provider's type. """

        provider_type = self.get_provider_type()

        if provider_type is None:
            instance.provider = None
            instance = super(EntitySerializer, self).update(instance, validated_data)
            return instance

        elif validated_data.get('type') <= provider_type:
            raise ValidationError({"detail": "Cannot specify a provider if it's lower in the hierarchy."})

        instance = super(EntitySerializer, self).update(instance, validated_data)
        return instance
