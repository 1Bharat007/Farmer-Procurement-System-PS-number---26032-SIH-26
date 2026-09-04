from django.db import models


class QueueToken(models.Model):
    """
    Live queue token issued to a farmer upon check-in at a procurement centre for a specific date.
    Tracks live queue position, token sequence, and operational status.
    """
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('called', 'Called to Gate/Weighbridge'),
        ('processing', 'Unloading & Quality Check'),
        ('completed', 'Completed'),
        ('skipped', 'Skipped / Delayed'),
    ]

    booking = models.OneToOneField(
        'bookings.Booking',
        on_delete=models.CASCADE,
        related_name='queue_token'
    )
    centre = models.ForeignKey(
        'centres.ProcurementCentre',
        on_delete=models.CASCADE,
        related_name='queue_tokens'
    )
    date = models.DateField(db_index=True)
    token_number = models.PositiveIntegerField(
        help_text="Sequential token number for the centre on this operating date"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='waiting',
        db_index=True
    )
    estimated_wait_minutes = models.PositiveIntegerField(
        default=0,
        help_text="Dynamically calculated estimated wait time in minutes"
    )
    called_at = models.DateTimeField(null=True, blank=True)
    served_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Queue Token"
        verbose_name_plural = "Queue Tokens"
        unique_together = ('centre', 'date', 'token_number')
        ordering = ['date', 'token_number']

    def __str__(self):
        return f"Token #{self.token_number} @ {self.centre.name} [{self.date}]: {self.status}"
