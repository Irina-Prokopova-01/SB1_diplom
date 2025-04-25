from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, permissions
from rest_framework.exceptions import PermissionDenied

from announcements.models import Announcement, Review
from announcements.paginators import AnnouncementPagination
from announcements.serializers import AnnouncementSerializer, ReviewSerializer
from users.permissions import IsOwner, IsAdmin


class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    Контроллер создания, просмотра, удаления, изменения обьявления.
    """
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = AnnouncementPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ["title"]

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            if self.request.user.is_authenticated:
                if self.request.user.role == "admin":
                    return [IsAdmin()]
                return [IsOwner()]
            raise PermissionDenied("У вас недостаточно прав!")
        return super().get_permissions()


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Контроллер создания, просмотра, удаления, изменения отзыва.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            if self.request.user.is_authenticated:
                if self.request.user.role == "admin":
                    return [IsAdmin()]
                return [IsOwner()]
            raise PermissionDenied("У вас недостаточно прав!")
        return super().get_permissions()
