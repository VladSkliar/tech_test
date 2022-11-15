from rest_framework.viewsets import ReadOnlyModelViewSet
from rental.models import Rental
from rental.serializers import RentalSerializer


class RentalViewSet(ReadOnlyModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    