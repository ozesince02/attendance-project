from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from .models import (
    TimetableEntry,
    AcademicCalendar,
    Holiday,
    AttendanceRule
)

from .serializers import (
    UserSerializer,
    TimetableEntrySerializer,
    AcademicCalendarSerializer,
    HolidaySerializer,
    AttendanceRuleSerializer
)

from .permissions import IsOwner


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model.
    NOTE: In a real application, you might restrict these operations
    (e.g., no listing all users, or only admin can do so).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Example: if you only want an authenticated user to view/update
        # their own user object, you might do:
        if self.request.user.is_authenticated:
            return User.objects.filter(id=self.request.user.id)
        return User.objects.none()


class TimetableEntryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for TimetableEntry. Only the owner can see/modify their entries.
    """
    serializer_class = TimetableEntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Return only the timetable entries belonging to the logged-in user
        return TimetableEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the 'user' field to the logged-in user
        serializer.save(user=self.request.user)


class AcademicCalendarViewSet(viewsets.ModelViewSet):
    """
    Each user typically has a single academic calendar (OneToOne).
    """
    serializer_class = AcademicCalendarSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return AcademicCalendar.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HolidayViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user-specific holidays.
    """
    serializer_class = HolidaySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Holiday.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AttendanceRuleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for attendance rules per subject for each user.
    """
    serializer_class = AttendanceRuleSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return AttendanceRule.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
