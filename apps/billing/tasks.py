from celery import shared_task
import time

@shared_task
def debug_task():
    """
    A simple debug task to verify Celery worker is processing tasks.
    """
    print("Debug task started...")
    time.sleep(2)
    print("Debug task finished!")
    return "Task Completed"
