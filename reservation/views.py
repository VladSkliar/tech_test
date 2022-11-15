from django.db.models import F
from django.db.models import OuterRef, Subquery
from rest_framework.viewsets import ReadOnlyModelViewSet

from reservation.models import Reservation
from reservation.serializers import ReservationSerializer


class ReservationViewSet(ReadOnlyModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filterset_fields = ['rental__name', 'rental_id']

    def get_queryset(self):
        prev_reservation = (
            Reservation.objects.filter(
                rental_id=OuterRef('rental_id'),
                checkout__lte=OuterRef('checkin')
            ).order_by('-checkout').values('id')
        )
        return Reservation.objects.annotate(
            rental_name=F('rental__name'),
            prev_reservation_id=Subquery(prev_reservation)
        )

