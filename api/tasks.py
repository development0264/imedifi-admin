
from celery.decorators import task
from celery.utils.log import get_task_logger
from time import sleep
from .models import Notification
from accounts.models import Country
from accounts.default_values import COUNTRIES


logger = get_task_logger(__name__)

# from django_celery_beat.models import PeriodicTask, PeriodicTasks
# PeriodicTask.objects.all().update(last_run_at=None)
# for task in PeriodicTask.objects.all():
#     PeriodicTasks.changed(task)

@task(name='read_notifications')
def read_notifications(notis):
    for n in notis:
        _n = Notification.objects.get(id=n['id'])
        print(_n)
        _n.visited = True
        _n.save()
    return True


@task(name='create_countries_list_default')
def create_countries_list_default():
    for code, name in COUNTRIES:
        c = Country(name=name, code=code)
        c.save()
    return True