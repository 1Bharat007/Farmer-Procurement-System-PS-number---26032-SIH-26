from celery import shared_task


@shared_task
def process_account_verification(user_id):
    """
    Placeholder async task for account verification / KYC processing.
    """
    return f"Account verification task executed for user_id={user_id}"
