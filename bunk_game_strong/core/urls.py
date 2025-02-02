from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    TimetableEntryViewSet,
    AcademicCalendarViewSet,
    HolidayViewSet,
    AttendanceRuleViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'timetable', TimetableEntryViewSet, basename='timetable')
router.register(r'academic-calendar', AcademicCalendarViewSet, basename='academic-calendar')
router.register(r'holidays', HolidayViewSet, basename='holiday')
router.register(r'attendance-rules', AttendanceRuleViewSet, basename='attendance-rule')

urlpatterns = [
    path('', include(router.urls)),
]
