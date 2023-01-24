from .models import SubTaskTaskRelations
from django.db.models import Avg, Count, Case, When


def set_timestamp(task):
    timestamp = SubTaskTaskRelations.objects.filter(task=task).aggregate(timestamp=Avg('time')).get('timestamp')
    task.timestamp = timestamp
    task.save()


def set_bool_count(task):
    bool_task = SubTaskTaskRelations.objects.filter(task=task).aggregate(count=Count(Case(When(bool=True, then=1))) +
                                                                               Count(Case(When(bool2=True, then=1)))).get('count')
    task.bool_count = bool_task
    task.save()
