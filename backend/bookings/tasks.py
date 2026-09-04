from celery import shared_task


@shared_task
def process_booking_reminder(booking_id):
    """
    Placeholder async task to send slot reminders to farmers.
    """
    return f"Booking reminder triggered for booking_id={booking_id}"
