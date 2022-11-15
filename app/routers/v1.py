from django.urls import path, include

api_router = [
    path('rentals/', include(('rental.routers.v1', 'rentals'), namespace='rentals')),
    path('reservations/', include(('reservation.routers.v1', 'reservations'), namespace='reservations'))
]