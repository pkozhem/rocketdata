from django.db.models import Avg
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from src.entities.models import Entity
from src.entities.serializers import EntitySerializer
from src.core.views import UpdateDestroyAPIView


class EntityListAPIView(ListAPIView):
    """ Returns list of all Entities and theirs data. """

    # permission_classes = [AllowAny]
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


class EntityDebtGreaterThanAverage(APIView):
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
