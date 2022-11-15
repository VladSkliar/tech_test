from rest_framework import routers
from reservation.views import ReservationViewSet

router = routers.SimpleRouter()
router.register(r'', ReservationViewSet, basename='reservation')

urlpatterns = router.urls
