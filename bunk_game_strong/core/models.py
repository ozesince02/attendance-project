from django.db import models
from django.contrib.auth.models import User

# If you want to store days of the week as choices:
DAY_CHOICES = [
    ('MON', 'Monday'),
    ('TUE', 'Tuesday'),
    ('WED', 'Wednesday'),
    ('THU', 'Thursday'),
    ('FRI', 'Friday'),
    ('SAT', 'Saturday'),
    ('SUN', 'Sunday'),
]

class TimetableEntry(models.Model):
    """
    Each record represents one class session on a particular day of the week,
    for a specific subject, with a custom start and end time.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='timetable_entries'
    )
    day_of_week = models.CharField(
        max_length=3,
        choices=DAY_CHOICES
    )
    subject = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()

    # Optionally add other fields, e.g. location, teacher, etc.

    def __str__(self):
        return (f"{self.subject} ({self.get_day_of_week_display()}) "
                f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}")


class AcademicCalendar(models.Model):
    """
    One-to-one mapping between a user and their academic year or semester range.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='academic_calendar'
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} Calendar: {self.start_date} to {self.end_date}"


class Holiday(models.Model):
    """
    A list of holidays or off-days where classes won't be held.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='holidays'
    )
    date = models.DateField()
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Holiday on {self.date} ({self.user.username}): {self.description}"


class AttendanceRule(models.Model):
    """
    Defines the minimum attendance percentage required per subject for a user.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='attendance_rules'
    )
    subject = models.CharField(max_length=100)
    minimum_percentage = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text="Enter value like 75.00 for 75% attendance requirement."
    )

    def __str__(self):
        return (f"{self.user.username} - {self.subject}: "
                f"Requires {self.minimum_percentage}%")
