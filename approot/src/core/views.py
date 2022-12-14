from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin


class UpdateDestroyAPIView(GenericAPIView,
                           UpdateModelMixin,
                           DestroyModelMixin):
    """ UD Generic API View. """

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
