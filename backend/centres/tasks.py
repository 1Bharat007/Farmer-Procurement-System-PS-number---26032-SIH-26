from celery import shared_task


@shared_task
def sync_procurement_centre_capacity(centre_id):
    """
    Placeholder async task to recalculate daily quota and intake capacity for a procurement centre.
    """
    return f"Capacity synced for centre_id={centre_id}"
