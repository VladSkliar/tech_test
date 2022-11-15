from rest_framework import routers
from rental.views import RentalViewSet

router = routers.SimpleRouter()
router.register(r'', RentalViewSet, basename='rental')

urlpatterns = router.urls
