from django.db import models
from django.conf import settings


class Notification(models.Model):
    """
    Automated notification dispatched to a farmer or operator (SMS, WhatsApp, In-App).
    """
    TYPE_CHOICES = [
        ('slot_confirmation', 'Slot Confirmation'),
        ('slot_reminder', 'Slot Reminder'),
        ('queue_called', 'Queue Called to Gate'),
        ('weather_advisory', 'Weather Advisory'),
        ('payment_disbursed', 'Payment Disbursed'),
        ('system_alert', 'System Alert'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        default='slot_confirmation'
    )
    is_read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification to {self.recipient.full_name}: {self.title}"
