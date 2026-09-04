import uuid
from django.db import models
from django.conf import settings


class Slot(models.Model):
    """
    Time-window reservation slot at a procurement centre for a specific date.
    """
    centre = models.ForeignKey(
        'centres.ProcurementCentre',
        on_delete=models.CASCADE,
        related_name='slots'
    )
    date = models.DateField(db_index=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.PositiveIntegerField(
        default=15,
        help_text="Maximum number of bookings allowed in this slot window"
    )
    booked_count = models.PositiveIntegerField(
        default=0,
        help_text="Current number of active bookings registered for this slot"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Slot"
        verbose_name_plural = "Slots"
        unique_together = ('centre', 'date', 'start_time', 'end_time')
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.centre.name} | {self.date} [{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}] ({self.booked_count}/{self.capacity})"

    @property
    def is_full(self):
        return self.booked_count >= self.capacity

    @property
    def available_capacity(self):
        return max(0, self.capacity - self.booked_count)


class Booking(models.Model):
    """
    Farmer slot reservation for crop intake and weighing at an MSP centre.
    """
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('checked_in', 'Checked In'),
        ('in_queue', 'In Queue'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    slot = models.ForeignKey(
        Slot,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='booked',
        db_index=True
    )
    quantity_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1000.00,
        help_text="Estimated crop quantity to be delivered in kilograms"
    )
    qr_code_token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True,
        help_text="Unique QR verification token presented at mandi intake gate"
    )
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking #{self.id}: {self.farmer.full_name} @ {self.slot.centre.name} ({self.status})"


class PaymentStatus(models.Model):
    """
    Financial disbursement record linked directly to a completed procurement booking.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='payment'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Direct Bank Transfer (DBT) payment amount in INR"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True
    )
    transaction_reference = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text="Bank UTR / PFMS / DBT transaction reference number"
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment Status"
        verbose_name_plural = "Payment Statuses"
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment for Booking #{self.booking_id}: ₹{self.amount} ({self.status})"
