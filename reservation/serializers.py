from rest_framework import serializers
from reservation.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    rental_name = serializers.CharField()
    prev_reservation_id = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Reservation
        fields = (
            'rental_name',
            'id',
            'checkin',
            'checkout',
            'prev_reservation_id'
        )