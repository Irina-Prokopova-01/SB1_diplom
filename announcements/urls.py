from django.urls import path, include
from rest_framework.routers import SimpleRouter
# from announcements.views import AnnouncementListAPIView
# from rest_framework.permissions import AllowAny

from .apps import AnnouncementsConfig
from announcements.views import AnnouncementViewSet, ReviewViewSet

app_name = AnnouncementsConfig.name

router = SimpleRouter()
router.register('', AnnouncementViewSet)
router.register('', ReviewViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

urlpatterns += router.urls