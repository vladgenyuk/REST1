from django.db import models
from django.contrib.auth.models import User


class SubTask(models.Model):
    title = models.CharField(max_length=50, null=True)
    desc = models.CharField(max_length=200, null=True)
    execute_time = models.IntegerField(null=True)

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField('название', max_length=50)
    task = models.TextField('описание')
    owner = models.ForeignKey(User, default=1, on_delete=models.PROTECT, null=True)
    subtask = models.ManyToManyField(SubTask, through='SubTaskTaskRelations', related_name='task')
    base_count = models.IntegerField(default=100)
    discount = models.IntegerField(null=True, blank=True)
    timestamp = models.DecimalField(max_digits=3, decimal_places=2, default=None, null=True)
    bool_count = models.DecimalField(max_digits=3, decimal_places=2, default=None, null=True)

    def __str__(self):
        return self.title


class SubTaskTaskRelations(models.Model):
    TIME_CHOICES = (
        (1, 'Ok'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible')
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    subtask = models.ForeignKey(SubTask, on_delete=models.CASCADE)
    char = models.CharField(max_length=255, blank=True)
    bool = models.BooleanField(default=False)
    bool2 = models.BooleanField(default=False)
    time = models.PositiveIntegerField(choices=TIME_CHOICES, null=True)

    def __str__(self):
        return f'{self.task}'

    def save(self, *args, **kwargs):
        old_timestamp = self.time
        creating = not self.pk

        super().save(*args, **kwargs)
        new_timestamp = self.time

        from .logic import set_timestamp, set_bool_count
        set_bool_count(self.task)

        if old_timestamp != new_timestamp or creating:
            set_timestamp(self.task)
