from django.core.management.base import BaseCommand
import schedule
import time
from parking.tasks import my_task

class Command(BaseCommand):
    help = 'Runs a scheduled task'

    def handle(self, *args, **options):
        # Schedule the task to run every 3 seconds
        schedule.every(1).seconds.do(my_task)

        # Run the scheduler loop
        while True:
            schedule.run_pending()
            time.sleep(1)