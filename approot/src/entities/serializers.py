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
    products = ProductSerializer(many=True, required=False)
    user = UserPublicSerializer(many=True, required=False)

    class Meta:
        model = Entity
        fields = '__all__'
        extra_kwargs = {
            "type": {
                "required": True,
                "read_only": False
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

    def get_provider_typ(self) -> int or None:
        """ Returns Entity provider's type, None if it doesn't exist. """

        provider_name: str or None = self.validated_data.get('provider')

        if provider_name is None:
            return None

        provider_type: int = list(Entity.objects.filter(name=provider_name).values('type'))[0].get('type')
        return provider_type

    def create(self, validated_data) -> Entity:
        """ Overwritten save method. Validates or not entity's/provider's type. """

        provider_id = self.get_provider_typ()

        if provider_id is None:
            entity = super(EntitySerializer, self).create(validated_data)
            return entity

        elif validated_data.get('type') <= provider_id:
            raise ValidationError({"detail": "Cannot specify a provider if it's lower or equal in the hierarchy."})

        entity = super(EntitySerializer, self).create(validated_data)
        return entity

    def update(self, instance, validated_data) -> Entity:
        """ Overwritten update method. Validates or not entity's/provider's type. """

        provider_id = self.get_provider_typ()

        if provider_id is None:
            instance.provider = None
            instance = super(EntitySerializer, self).update(instance, validated_data)
            return instance

        elif validated_data.get('type') <= provider_id:
            raise ValidationError({"detail": "Cannot specify a provider if it's lower in the hierarchy."})

        instance = super(EntitySerializer, self).update(instance, validated_data)
        return instance
