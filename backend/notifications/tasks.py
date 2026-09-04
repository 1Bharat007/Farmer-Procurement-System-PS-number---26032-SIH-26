from celery import shared_task


@shared_task
def send_sms_notification(phone_number, message):
    """
    Placeholder async task for sending SMS/WhatsApp notifications to farmers.
    """
    return f"Notification sent to {phone_number}: {message}"
