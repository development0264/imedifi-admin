
from celery.decorators import task
from celery.utils.log import get_task_logger
from time import sleep
from .models import Query

logger = get_task_logger(__name__)

# from django_celery_beat.models import PeriodicTask, PeriodicTasks
# PeriodicTask.objects.all().update(last_run_at=None)
# for task in PeriodicTask.objects.all():
#     PeriodicTasks.changed(task)


