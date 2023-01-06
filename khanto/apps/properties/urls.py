from rest_framework import routers
from properties.views import PropertyViewSet, AnnouncementViewSet

router = routers.DefaultRouter()

router.register("properties", PropertyViewSet)
router.register("announcements", AnnouncementViewSet)

urlpatterns = router.urls
