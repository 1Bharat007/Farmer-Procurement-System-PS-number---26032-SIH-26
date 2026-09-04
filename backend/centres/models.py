from django.db import models


class ProcurementCentre(models.Model):
    """
    Government Minimum Support Price (MSP) grain procurement centre / mandi.
    """
    name = models.CharField(max_length=200, help_text="e.g. Karnal Central Grain Procurement Centre")
    address = models.TextField(help_text="Full physical address or landmark")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    district = models.CharField(max_length=100, db_index=True)
    state = models.CharField(max_length=100, default="Haryana")
    daily_capacity = models.PositiveIntegerField(
        default=80,
        help_text="Maximum number of booking tokens/deliveries handled per operating day"
    )
    avg_processing_time_minutes = models.PositiveIntegerField(
        default=25,
        help_text="Average processing, weighing, and QC time in minutes per farmer trolley"
    )
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Procurement Centre"
        verbose_name_plural = "Procurement Centres"
        ordering = ['district', 'name']

    def __str__(self):
        return f"{self.name} ({self.district}, {self.state})"


class OperatingHours(models.Model):
    """
    Weekly operating hours and open/closed status for a procurement centre.
    """
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    centre = models.ForeignKey(
        ProcurementCentre,
        on_delete=models.CASCADE,
        related_name='operating_hours'
    )
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    opening_time = models.TimeField(default="08:00:00")
    closing_time = models.TimeField(default="16:00:00")
    is_closed = models.BooleanField(
        default=False,
        help_text="True if centre is closed on this day (e.g. Sundays)"
    )

    class Meta:
        verbose_name = "Operating Hours"
        verbose_name_plural = "Operating Hours"
        unique_together = ('centre', 'day_of_week')
        ordering = ['centre', 'day_of_week']

    def __str__(self):
        day_name = dict(self.DAYS_OF_WEEK).get(self.day_of_week, f"Day {self.day_of_week}")
        if self.is_closed:
            return f"{self.centre.name} - {day_name}: CLOSED"
        return f"{self.centre.name} - {day_name}: {self.opening_time.strftime('%H:%M')} - {self.closing_time.strftime('%H:%M')}"
