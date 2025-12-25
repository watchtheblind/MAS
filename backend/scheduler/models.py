from django.db import models


class DayOfWeek(models.TextChoices):
    """Days of the week"""
    MONDAY = 1, 'Monday'
    TUESDAY = 2, 'Tuesday'
    WEDNESDAY = 3, 'Wednesday'
    THURSDAY = 4, 'Thursday'
    FRIDAY = 5, 'Friday'
    SATURDAY = 6, 'Saturday'
    SUNDAY = 7, 'Sunday'
# Create your models here.
class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    medic_id = models.ForeignKey('users.Medics', on_delete=models.CASCADE, null=False)
    center_id = models.ForeignKey('appointments.Center', on_delete=models.CASCADE, null=False)
    day_of_week = models.CharField(max_length=10, choices=DayOfWeek.choices)
    start_time = models.DateTimeField(
        verbose_name="Start time",
        help_text="Date and time of exception beginning"
    )
    end_time = models.DateTimeField(
        verbose_name="End time",
        help_text="Date and time of exception ending"
    )
    max_patients_per_day = models.PositiveIntegerField()
    appointments_minute_interval = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

class ScheduleExceptions(models.Model):
    class ScheduleExceptionType(models.TextChoices):
        """schedule exception types"""
        # Health
        SICK_LEAVE = 'sick_leave'
        MEDICAL_APPOINTMENT = 'medical_appointment'
        MATERNITY_LEAVE = 'maternity_leave'
        # Vacations
        VACATION = 'vacation'
        PERSONAL_DAY = 'personal_day'
        # Emergencies
        FAMILY_EMERGENCY = 'family_emergency'
        BEREAVEMENT = 'bereavement'
        # Work
        TRAINING = 'training'
        CONFERENCE = 'conference'
        ON_CALL = 'on_call', 'Guardia'
        # Others
        TRANSPORT_ISSUE = 'transport_issue'
        WEATHER = 'weather', 'Clima'
        OTHER = 'other'
    id = models.AutoField(primary_key=True)
    medic_id = models.ForeignKey('users.Medics', on_delete=models.CASCADE, null=False, related_name='schedule_exceptions')
    date = models.DateField(
        null=False,
        blank=False,
        verbose_name='Date of exception',
        help_text='Insert the date of exception',
    )
    exception_type = models.CharField(
        max_length=50,
        choices=ScheduleExceptionType.choices,
        default=ScheduleExceptionType.OTHER,
        null=False
    )
    description = models.TextField()
    whole_day = models.BooleanField()
    start_time = models.DateTimeField(
        verbose_name="Start time",
        help_text="Date and time of exception beginning"
    )
    end_time = models.DateTimeField(
        verbose_name="End time",
        help_text="Date and time of exception ending"
    )



