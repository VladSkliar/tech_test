from rest_framework import serializers
from rental.models import Rental


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = (
            'id',
            'name'
        )
