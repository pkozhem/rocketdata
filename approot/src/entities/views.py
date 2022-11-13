from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from src.entities.models import Entity, Contacts
from src.entities.serializers import EntitySerializer, ContactsSerializer
from src.entities.tasks import send_email_worker
from src.core.views import UpdateDestroyAPIView
from src.core.functions import make_qrcode


class EntityListAPIView(ListAPIView):
    """ Returns list of all Entities and theirs data. """

    serializer_class = EntitySerializer

    def get_queryset(self):
        return Entity.objects.select_related('contacts', 'contacts__address', 'provider') \
            .prefetch_related('products', 'user').order_by('id')


class EntityCountryAPIView(APIView):
    """ Returns Entities by Address country which is entered in url params like .../country?name={string} """

    def get(self, request):
        country_name = request.query_params.get('name')

        if country_name == '':
            return Response({"details": "Input country name."})

        queryset = Entity.objects.select_related('contacts', 'contacts__address', 'provider') \
            .prefetch_related('products', 'user').filter(contacts__address__country=country_name).order_by('id')
        serializer = EntitySerializer(queryset, many=True)
        return Response(serializer.data)


class EntityDebtGreaterThanAvgAPIView(APIView):
    """ Returns Entities with debt more than average debt among all Entities. """

    def get(self, request):
        base_queryset = Entity.objects.select_related('contacts', 'contacts__address', 'provider') \
            .prefetch_related('products', 'user')

        average_debt = list(base_queryset.aggregate(Avg('debt')).values())[0]
        result_queryset = base_queryset.filter(debt__gt=average_debt).order_by('id')
        serializer = EntitySerializer(result_queryset, many=True)
        return Response(serializer.data)


class EntityByProductIDAPIView(APIView):
    """ Returns Entities by Product id which is entered url params like .../product?id={int} """

    def get(self, request):
        product_id = request.query_params.get('id')

        if product_id == '':
            return Response({"details": "Input product id."})

        queryset = Entity.objects.select_related('contacts', 'contacts__address', 'provider') \
            .prefetch_related('products', 'user').filter(products__id=product_id).order_by('id')
        serializer = EntitySerializer(queryset, many=True)
        return Response(serializer.data)


class EntityRetrieveAPIView(APIView):
    """ Entity retrieve API view. Returns Entity to which request user belongs """

    def get(self, request):
        queryset = Entity.objects.select_related('contacts', 'contacts__address', 'provider') \
            .prefetch_related('products', 'user').filter(user=request.user)
        serializer = EntitySerializer(queryset, many=True)
        return Response(serializer.data)


class EntityCreateAPIView(CreateAPIView):
    """ Entity create API view. """

    serializer_class = EntitySerializer

    def get_queryset(self):
        return Entity.objects.select_related('contacts', 'contacts__address', 'provider') \
            .prefetch_related('products', 'user')


class EntityUpdateDestroyAPIView(UpdateDestroyAPIView):
    """ Entity UD API View. """

    serializer_class = EntitySerializer

    def get_queryset(self):
        return Entity.objects.select_related('contacts', 'contacts__address', 'provider') \
            .prefetch_related('products', 'user').filter(id=self.kwargs['pk'])


class ContactsQRCode(APIView):
    """ Generates QR Code by Entity's address. """

    def get(self, request, pk):
        queryset = Contacts.objects.filter(entity=self.kwargs['pk'])
        serializer = ContactsSerializer(queryset, many=True)
        make_qrcode(serializer.data[0], pk)
        send_email_worker.delay(request.user.email, pk)
        return Response({"detail": "QR code has sent to your email."})
