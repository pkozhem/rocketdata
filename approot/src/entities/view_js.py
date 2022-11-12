from django.views.generic.list import ListView
from src.entities.models import Entity


class EntityListView(ListView):
    """ Shows all Entities. """

    template_name = 'entities/index.html'

    def get_queryset(self):
        return Entity.objects.select_related('contacts', 'contacts__address', 'provider') \
            .prefetch_related('products', 'user').order_by('id')
